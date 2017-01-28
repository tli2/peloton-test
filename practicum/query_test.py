import os
import shutil
import sys
import logging
import common
import psycopg2
from ConfigParser import RawConfigParser
LOG = common.LOG
LOG = logging.getLogger()
LOG_handler = logging.StreamHandler()
LOG_formatter = logging.Formatter(fmt='%(asctime)s [%(funcName)s:%(lineno)03d] %(levelname)-5s: %(message)s',
                                  datefmt='%m-%d-%Y %H:%M:%S')
LOG.setLevel(logging.INFO)

basedir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "..", ".."))
configPath = os.path.realpath(os.path.join(os.pardir, "test.conf-sample"))

class QueryTest(object):
    def __init__(self, configPath, dbs, tableScript=None, testScript=None):
        # Load in configuration file
        LOG.info("Loading config file '%s'" % configPath)
        self.config = RawConfigParser()
        self.config.read(configPath)
        self.connections = 0
        self.dbs=dbs
        self.tableScript = tableScript
        self.testScript = testScript
        # connect to dbs
        for db in self.dbs:
            try:
                self.__dict__[db] = psycopg2.connect(
                    host=self.config.get(db, 'db_host'),
                    port=self.config.get(db, 'db_port'),
                    database=self.config.get(db, 'db_name'),
                    user=self.config.get(db, 'db_user'),
                    password=self.config.get(db, 'db_pass'),
                )
                LOG.info("connected to {}".format(db.upper()))
                assert (not self.__dict__[db] is None)
                LOG.debug("connected to %s database" % db.upper())
                self.connections += 1
            except:
                LOG.error("unable to connect to %s database" % db.upper())

    def closeConnections(self):
        for db in self.dbs:
            if self.__dict__[db] is not None:
                self.__dict__[db].close()
                LOG.info("closed database {}".format(db.upper()))

    def queryTest(self):
        if os.path.exists(os.path.realpath(os.path.join(os.pardir, "test_script_result"))):
            shutil.rmtree(os.path.realpath(os.path.join(os.pardir, "test_script_result")))
        os.makedirs(os.path.realpath(os.path.join(os.pardir, "test_script_result")))
        for db in self.dbs:
            try:
                file_read = open("../scripts/" + self.testScript)
                file_write = open(os.path.join(os.path.realpath(os.path.join(os.pardir, "test_script_result")),
                                                db + ".txt"),'w+')
                conn = self.__dict__[db]; cur = conn.cursor()
                prev = None
                for line in file_read:
                    cur.execute(line)
                    rows = cur.fetchall()
                    if prev is not None: file_write.write("\n")
                    for row in rows:
                        file_write.write(str(row))
                    prev = line
                file_read.close()
                file_write.close()
                LOG.info("query commands for %s database completed" % db.upper())
            except:
                LOG.error("cannot perform commands to %s database" % db.upper())

    def buildTestTables(self):
        for db in self.dbs:
            try:
                conn = self.__dict__[db]; cur = conn.cursor()
                # temporary solution
                cur.execute("drop schema public cascade")
                cur.execute("create schema public")
                file = open("../scripts/" + self.tableScript)
                for line in file:
                    cur.execute(line)
                file.close()
                conn.commit()
                LOG.info("tables created for {}".format(db.upper()))
            except:
                LOG.error("cannot perform table creation to %s database" % db.upper())

    def dropTables(self):
        pass

#======================================================================================
dbs = ["oracle", "target"]
tableScriptPath = "tableScript.txt"
testScriptPath = "testScript.txt"
test_obj = QueryTest(configPath, dbs, tableScriptPath, testScriptPath)
test_obj.buildTestTables()
test_obj.queryTest()
test_obj.closeConnections()
from test_modules_prac import generate_tables
import os
import shutil
import sys
import logging
import psycopg2
from ConfigParser import RawConfigParser
LOG = logging.getLogger()
LOG_handler = logging.StreamHandler()
LOG_formatter = logging.Formatter(fmt='%(asctime)s [%(funcName)s:%(lineno)03d] %(levelname)-5s: %(message)s',
                                  datefmt='%m-%d-%Y %H:%M:%S')
LOG.setLevel(logging.INFO)

basedir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "..", ".."))
configPath = os.path.realpath(os.path.join(os.pardir, "test.conf-sample"))

class BaseTest(object):
    def __init__(self, configPath, dbs, query_count=10):
        # Load in configuration file
        LOG.info("Loading config file '%s'" % configPath)
        self.config = RawConfigParser()
        self.config.read(configPath)
        self.connections = 0
        self.dbs=dbs
        self.query_count = query_count
        self.table_names = None
        self.table_cols = None

    def setupConnections(self):
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

    def getTableNames(self):
        table_names = []
        for db in self.dbs:
            conn = self.__dict__[db]
            cur = conn.cursor()
            cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
            name_tuples = cur.fetchall()
            table_names_current = []
            for tuple in name_tuples:
                table_names_current.append(tuple[0])
            table_names.append(table_names_current)
        self.table_names = table_names

    def getTableCols(self):
        table_cols = []
        oracle = self.dbs[0]
        conn = self.__dict__[oracle]
        cur = conn.cursor()
        for table in self.table_names:
            query = "SELECT * FROM {}".format(str(table))
            cur.execute(query)
            col_names = [desc[0] for desc in cur.description]
            table_cols.append(col_names)
        self.table_cols = table_cols

    def dropTables(self):
        for i in range(len(self.dbs)):
            try:
                conn = self.__dict__[self.dbs[i]];
                cur = conn.cursor()
                db_table_names = self.table_names[i]
                for name in db_table_names:
                    cur.execute("DROP TABLE {}".format(name))
                conn.commit()
                LOG.info("tables dropped {}".format(self.dbs[i]).upper())
            except:
                LOG.error("unable to drop tables {}".format(self.dbs[i].upper()))

    def buildTestTables(self):
        generate_tables.buildRandomTestTables(self, LOG, self.query_count)



#======================================================================================
"""
dbs = ["oracle", "target"]
test_obj = QueryTest(configPath, dbs)
test_obj.dropTables()
test_obj.buildTestTables()
test_obj.closeConnections()
"""

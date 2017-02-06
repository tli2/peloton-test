from nose import with_setup
from unittest import TestCase
import BaseTestSetup
import os
import sys
from test_modules_prac import randop

basedir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "..", ".."))
configPath = os.path.realpath(os.path.join(os.pardir, "test.conf-sample"))

# setup the databases
dbs = ["oracle", "target"]
test_obj = BaseTestSetup.BaseTest(configPath, dbs)
test_obj.setup_connections()
test_obj.get_table_names()
test_obj.drop_tables()
test_obj.build_test_tables()
test_obj.get_table_cols()


class TestSelect(TestCase):

    def setup(self):
        pass

    def test_select_star(self):
        print("\nTest -> SELECT * FROM CORP")
        query = """SELECT * FROM CORP"""
        print("\t{}".format(query))
        conn = test_obj.__dict__[test_obj.dbs[0]]
        cur = conn.cursor()
        cur.execute(query)
        rows_oracle = cur.fetchall()
        for db in test_obj.dbs[1:]:
            conn = test_obj.__dict__[db]
            cur = conn.cursor()
            cur.execute(query)
            rows_target = cur.fetchall()
            assert(rows_oracle == rows_target)

    def test_select_cols(self):
        print("\nTest -> SELECT col FROM CORP")
        for col in test_obj.table_cols[0]:
            query="SELECT {} FROM CORP".format(str(col))
            print("\t{}".format(query))
            conn = test_obj.__dict__[test_obj.dbs[0]]
            cur = conn.cursor()
            cur.execute(query)
            rows_oracle = cur.fetchall()
            for db in test_obj.dbs[1:]:
                conn = test_obj.__dict__[db]
                cur = conn.cursor()
                cur.execute(query)
                rows_target = cur.fetchall()
                assert (rows_oracle == rows_target)

    def test_arithmetic(self):
        print("\nTest -> SELECT arithmetic")
        a = randop.create_random_int(1,10); b = randop.create_random_int(1,10)
        expression = "{} + {}".format(a,b)
        query = "SELECT {}".format(expression)
        print("\t{}".format(query))
        conn = test_obj.__dict__[test_obj.dbs[0]]
        cur = conn.cursor()
        cur.execute(query)
        rows_oracle = cur.fetchall()
        results = []
        for tuple in rows_oracle:
            results.append(tuple[0])
        assert results[0] == (a+b)

    def tearDow(self):
        pass



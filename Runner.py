import os
import sys
import unittest

from common.base_test import BaseTest
from generate.query_generator import QueryGenerator

basedir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(basedir, "..")))
tests_path = os.path.realpath(os.path.join(os.pardir, "peloton-test/tests"))
config_path = os.path.realpath(os.path.join(os.pardir, "peloton-test/test.conf"))
dbs = ["oracle", "target"]

query_generator = QueryGenerator()


def setup():
    test_obj = BaseTest(config_path, dbs)
    test_obj.setup_connections()
    test_obj.get_table_names()
    test_obj.drop_tables()
    test_obj.build_test_tables()
    test_obj.get_table_cols()
    return test_obj


def teardown(test_obj):
    test_obj.close_connections()


class TestsContainer(unittest.TestCase):
    longMessage = True


def make_test_function(queries):
    for query in queries:
        test_obj = setup()
        def test(self):
            conn = test_obj.__dict__[self.dbs[0]]
            cur = conn.cursor()
            cur.execute(query)
            rows_oracle = cur.fetchall()
            for db in test_obj.dbs[1:]:
                conn = test_obj.__dict__[db]
                cur = conn.cursor()
                cur.execute(query)
                rows_target = cur.fetchall()
                assert (rows_oracle == rows_target)
            teardown(test_obj)
    return test


def files_in_dir(target_dir):
    for subdir, dirs, files in os.walk(target_dir):
        for one_file in files:
            yield subdir + os.sep + one_file


if __name__ == '__main__':
    print tests_path
    for test_file in files_in_dir(tests_path):
        print test_file
        setattr(TestsContainer, test_file, make_test_function(query_generator.get_queries(test_file)))

    unittest.main()

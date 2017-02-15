import os
import sys
from unittest import TestCase

from common import randop, base_test
from runner import base_test


class TestSelectQuery(TestCase):
    @classmethod
    def setUpClass(cls):
        basedir = os.path.realpath(os.path.dirname(__file__))
        sys.path.append(os.path.join(basedir, "..", ".."))
        config_path = os.path.realpath(os.path.join(os.pardir, "test.conf"))

        global test_obj
        dbs = ["oracle", "target"]
        test_obj = base_test.BaseTest(config_path, dbs)
        test_obj.setup_connections()
        test_obj.get_table_names()
        test_obj.drop_tables()
        test_obj.build_test_tables()
        test_obj.get_table_cols()

        global table_columns
        table_columns = test_obj.table_cols

        global table_column_types
        table_column_types = test_obj.table_col_types

        global operators
        operators = ['=', '!=', '>', '<', '>=', '<=']

    @classmethod
    def tearDownClass(cls):
        print("\n")
        test_obj.close_connections()

    def test_select_star(self):
        print("\nTest -> SELECT * FROM CORP")
        query = """SELECT * FROM CORP"""
        print("\t{}".format(query))
        test_obj.run_query(query)

    def test_select_cols(self):
        print("\nTest -> SELECT *col* FROM CORP")
        for col in test_obj.table_cols[0]:
            query = "SELECT {} FROM CORP".format(str(col))
            print("\t{}".format(query))
            test_obj.run_query(query)

    def test_arithmetic(self):
        print("\nTest -> SELECT *arithmetic*")
        a_values = [randop.create_random_int(1, 10), randop.create_random_float(1, 10)]
        b_values = [randop.create_random_int(1, 10), randop.create_random_float(1, 10)]
        for a, b in zip(a_values, b_values):
            expression = "{} + {}".format(a, b)
            query = "SELECT {}".format(expression)
            print("\t{}".format(query))
            test_obj.run_query(query)

    def test_where_1(self):
        print("\nTest -> SELECT * FROM CORP WHERE *col* *operator* *value*")
        int_values = [0] * len(operators)
        float_values = [0] * len(operators)
        col_values = [0] * len(operators)
        columns = table_columns[0]
        types = table_column_types[0]
        int_cols = [columns[i] for i in range(len(types))
                    if types[i] == 23]
        for i in range(len(operators)):
            int_values[i] = randop.create_random_int(1, 20)
            float_values[i] = randop.create_random_float(1, 20)
            col_values[i] = int_cols[randop.create_random_int(0, len(int_cols) - 1)]
        for i in range(len(operators)):
            query = "SELECT * FROM CORP WHERE {} {} {}"
            query = query.format(col_values[i], operators[i], int_values[i])
            print("\t{}".format(query))
            test_obj.run_query(query)
            query = "SELECT * FROM CORP WHERE {} {} {}"
            query = query.format(col_values[i], operators[i], float_values[i])
            print("\t{}".format(query))
            test_obj.run_query(query)

    def test_where_in(self):
        print("\nTest -> SELECT * FROM CORP WHERE *col* IN *(values)*")
        columns = table_columns[0]
        types = table_column_types[0]
        string_cols = [columns[i] for i in range(len(types))
                       if types[i] == 1043]
        string_cols *= 10
        fuzz2 = []
        for i in range(len(string_cols)):
            x = randop.create_random_int(0, 15)
            fuzz2.append((randop.create_random_string(x), randop.create_random_string(x)))
        for i in range(len(string_cols)):
            query = "SELECT * FROM CORP WHERE {} IN {}".format(string_cols[i], fuzz2[i])
            print("\t{}".format(query))
            test_obj.run_query(query)

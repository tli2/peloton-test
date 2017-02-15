import itertools
import os
import sys
from unittest import TestCase

from practicum.test_modules_prac import randop

from runner import BaseTestSetup


class TestSelectRandom(TestCase):
    @classmethod
    def setUpClass(cls):
        basedir = os.path.realpath(os.path.dirname(__file__))
        sys.path.append(os.path.join(basedir, "..", ".."))
        configPath = os.path.realpath(os.path.join(os.pardir, "test.conf-sample"))

        global breakLine
        breakLine="====="*20

        global debug
        debug=True

        global test_obj
        dbs = ["oracle", "target"]
        test_obj = BaseTestSetup.BaseTest(configPath, dbs)
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

        global operators_more
        operators_more = ['=', '!=', '>', '<', '>=', '<=','IN']

        global string_cols
        string_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
                       if table_column_types[0][i] == 1043]

        global int_cols
        int_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
                       if table_column_types[0][i] == 23]

    @classmethod
    def tearDownClass(cls):
        print("\n{}".format(breakLine))
        test_obj.close_connections()

    def test_select_random(self):
        query="SELECT {0}{1}{2} FROM CORP WHERE {3} {4} {5}"
        if debug:
            print("\n{}".format(breakLine))
            print("Test -> {}\n".format(query))
        # this covers combinations for {0}{1}{2}
        col_combinations=[]
        combinations_cols=[]
        for x in range(len(table_columns[0])):
            col_combinations.append(itertools.combinations(table_columns[0], x))
        for x in range(1,len(col_combinations)):
            for comb in col_combinations[x]:
                if x != len(col_combinations) - 1:
                    comb += ('',)*((len(col_combinations)-1)-x)
                combinations_cols.append(comb)
        # this covers options for {3}
        # made global string_cols and string_ints
        # this covers options for {4}
        combinations_cols4=[op for op in operators]
        combinations_cols4_more=[op for op in operators_more]
        # this covers options for {5}
        random_strings=[]
        random_ints=[]
        random_floats=[]
        for i in range(100):
            random_strings+=[randop.create_random_string(randop.create_random_int(1, 20))]
            random_ints+=[randop.create_random_int(-100, 100)]
            random_floats+=[randop.create_random_float(-100, 100)]
        # query loop
        iterations=10
        while iterations:
            iterations-=1
            query = "SELECT {0}{1}{2} FROM CORP WHERE {3} {4} {5}"
            # obtain indexes
            index_cols= randop.create_random_int(0, len(combinations_cols) - 1)
            index_cols3_string= randop.create_random_int(0, len(string_cols) - 1)
            index_cols3_int= randop.create_random_int(0, len(int_cols) - 1)
            index_cols4= randop.create_random_int(0, len(combinations_cols4) - 1)
            index_cols4_more= randop.create_random_int(0, len(combinations_cols4_more) - 1)
            index_strings= randop.create_random_int(0, len(random_strings) - 1)
            index_ints= randop.create_random_int(0, len(random_ints) - 1)
            index_floats= randop.create_random_int(0, len(random_floats) - 1)
            # obtain formatting values
            zero=combinations_cols[index_cols][0]
            one=combinations_cols[index_cols][1]
            if one:
                one=","+one
            two=combinations_cols[index_cols][2]
            if two:
                two=","+two
            three_string=string_cols[index_cols3_string]
            three_int=int_cols[index_cols3_int]
            four=combinations_cols4[index_cols4]
            four_string=combinations_cols4_more[index_cols4_more]
            string="('"+random_strings[index_strings]+"')"
            int=random_ints[index_ints]
            float=random_floats[index_floats]
            # string query
            query_string=query.format(zero,one,two,three_string,four_string,string)
            if debug:
                print("\t{}".format(query_string))
            test_obj.run_query(query_string)
            query_int=query.format(zero,one,two,three_int,four,int)
            if debug:
                print("\t{}".format(query_int))
            test_obj.run_query(query_int)
            query_float=query.format(zero,one,two,three_int,four,float)
            if debug:
                print("\t{}\n".format(query_float))
            test_obj.run_query(query_float)

import itertools
import os
import sys
import pprint
from common import randop
from unittest import TestCase

from common import randop, base_test

pp = pprint.PrettyPrinter()

test_obj = None

basedir = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, "..", ".."))
configPath = os.path.realpath(os.path.join(os.pardir, "test.conf-sample"))

debug = True

dbs = ["oracle", "target"]
test_obj = base_test.BaseTest(configPath, dbs)
test_obj.setup_connections()
test_obj.get_table_names()
test_obj.drop_tables()
test_obj.build_test_tables()
test_obj.get_table_cols()

table_columns = test_obj.table_cols

table_column_types = test_obj.table_col_types

operators = ['=', '!=', '>', '<', '>=', '<=']

operators_more = ['=', '!=', '>', '<', '>=', '<=', 'IN']

string_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
               if table_column_types[0][i] == 1043]

int_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
            if table_column_types[0][i] == 23]



def sample_build():
    query = "SELECT "
    number_cols = len(string_cols) + len(int_cols)
    query += "{}" * number_cols
    query += " FROM CORP WHERE {} {} {}"
    if debug:
        print("Test -> {}\n".format(query))

def gen_col_options_build():
    # this covers options for the cols or the options for the left hand side
    col_combinations = []
    comb_permutations_cols = []
    for x in range(len(table_columns[0])):
        col_combinations.append(itertools.combinations(table_columns[0], x))
    for x in range(1, len(col_combinations)):
        for comb in col_combinations[x]:
            for z in itertools.permutations(comb):
                if z != len(col_combinations) -1:
                    z += ('',) * ((len(col_combinations) - 1) - x)
                yield z

def where_options_build(type):
    if type == "VarChar":
        query_formatting = None
        for x in string_cols:
            for y in operators_more:
                query_formatting = [x]
                query_formatting.append(y)
                if y == 'IN':
                    temp_string = randop.create_random_string(randop.create_random_int(1,20))
                    query_formatting.append("(" + temp_string + ")")
                else:
                    query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))
                yield tuple(query_formatting)
        pass
    elif type == "Int":
        pass

sample_build()

# String col testing
for x in gen_col_options_build():
    print x
    for z in where_options_build("VarChar"):
        print z
    print("---")

print(x)





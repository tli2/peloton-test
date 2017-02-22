import itertools
import os
import sys
import pprint
from common import randop
from common import query_generate_columns
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
###########################################################################################


def statement_gen(statement):
    loc=0
    if statement[loc]== "Data Manipulation Statement":
        loc+=1
        if statement[loc]== "SELECT":
            loc+=1
            return "SELECT "
    return ''

def col_holders():
    number_cols = len(string_cols) + len(int_cols)
    return "{}" * number_cols + " "

def clause_gen(clause):
    loc=0
    if len(clause[loc:]) > 0 and clause[loc] == "FROM":
        loc+=1
        if len(clause[loc:]) > 0 and clause[loc] == "WHERE":
            loc+=1
            return "FROM "+ TABLE + " WHERE "
    return ''

def predicate_gen(predicate):
    loc=0
    if len(predicate[loc:]) > 0 and predicate[loc] == "JOIN":
        return "JOIN "
    return ''

def expression_gen(expression):
    loc=0
    if len(expression[loc:]) > 0 and expression[loc] == "Case Expression":
        pass
    return ''

def operator_gen(operator):
    loc=0
    # should have a way to set the place holder positions
    if len(operator[loc])>0 and operator[loc] == "Arithemic":
        return ['=', '!=', '>', '<', '>=', '<=']
    return ''

def sample_build(statement,clause,predicate,expression,operator):

    # the name of the table
    global TABLE
    TABLE = "CORP"

    # types of columns
    col_types = ["VarChar","Int"]

    # obtain the raw statement
    query_statement_raw = ""
    query_statement_raw += statement_gen(statement)

    # obtain the raw clause
    query_clause_raw = ""
    query_clause_raw += clause_gen(clause)
    query_clause_raw += predicate_gen(predicate)
    query_clause_raw += expression_gen(expression)

    # format the query
    for col_type in col_types:
        for x in query_generate_columns.generate_column_options(table_columns):
            query_statement = query_statement_raw
            query_statement += x
            rules = operator_gen(operator)
            for y in query_clause_generation(col_type,rules):
                query_clause = query_clause_raw
                query_clause+=y
                query_formatted=query_statement + ' ' + query_clause
                print(query_formatted)
                break
            break
        break

def query_clause_generation(col_type,rules):
    if col_type == "VarChar":
        query_formatting = None
        for x in string_cols:
            for y in rules:
                query_formatting = [x]
                query_formatting.append(y)
                if y == 'IN':
                    temp_string = randop.create_random_string(randop.create_random_int(1,20))
                    query_formatting.append("(" + temp_string + ")")
                else:
                    query_formatting.append(randop.create_random_string(randop.create_random_int(1, 20)))
                return_string=""
                for i in range(len(query_formatting)):
                    if i > 0:
                        return_string+=" " + query_formatting[i]
                    else:
                        return_string+=query_formatting[i]
                yield return_string
    elif col_type == "Int":
        pass

##################################################################################################
statement = ["Data Manipulation Statement", "SELECT"]
clause = ["FROM","WHERE"]
predicate = []
expression = []
operator = ["Arithemic"]
sample_build(statement,clause,predicate,expression,operator)






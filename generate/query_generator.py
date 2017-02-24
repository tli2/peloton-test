from common import base_test
from generate import query_generate_clause
from generate import query_generate_columns
from generate import query_generate_operator
from generate import clause_generate
from generate import statement_generate
from generate import expression_generate
from generate import predicate_generate



class QueryGenerator:
    def __init__(self, table, cols, col_types):
        global TABLE
        TABLE = table
        global table_columns
        table_columns = cols
        global table_column_types
        table_column_types = col_types

        string_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
                       if table_column_types[0][i] == 1043]
        int_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
                    if table_column_types[0][i] == 23]

        global column_split
        column_split = [string_cols, int_cols]

    # TODO: change this to an actual generator
    def get_queries(self, test_file=None):
        # parse into a format below
        statement = ["Data Manipulation Statement", "SELECT"]
        clause = ["FROM", "WHERE"]
        predicate = []
        expression = []
        # operator = ["Comparison", "Conjunction"]
        operator = ["Comparison"]

        return self.get_queries_helper(statement, clause, predicate, expression, operator)

    @staticmethod
    def get_queries_helper(statement, clause, predicate, expression, operator):

        # types of columns
        col_types = ["VarChar", "Int"]

        # obtain the raw statement
        query_statement_raw = ""
        query_statement_raw += statement_generate.statement_gen(statement)

        # obtain the raw clause
        query_clause_raw = ""
        query_clause_raw += clause_generate.clause_gen(clause)
        query_clause_raw += predicate_generate.predicate_gen(predicate)
        query_clause_raw += expression_generate.expression_gen(expression)

        # format the query
        for col_type in col_types:
            for x in query_generate_columns.generate_column_options(table_columns):
                query_statement = query_statement_raw
                query_statement += x
                rules = query_generate_operator.operator_gen(operator)
                for y in query_generate_clause.generate_clause(column_split, col_type, rules):
                    query_clause = query_clause_raw
                    query_clause += y
                    query_formatted = query_statement + ' ' + query_clause
                    yield query_formatted

from common import base_test
from generate import query_clause_generation
from generate import query_column_generation
from generate import operator_generate
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
        global string_cols
        string_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
                       if table_column_types[0][i] == 1043]
        global int_cols
        int_cols = [table_columns[0][i] for i in range(len(table_column_types[0]))
                    if table_column_types[0][i] == 23]
        global column_split
        column_split = [string_cols, int_cols]

    def get_queries(self, test_file=None):
        # parse into a format below

        statement = ["Data Manipulation Statement", "SELECT"]
        clause = ["FROM", "WHERE"]
        predicate = []
        expression = ["Aggregate","Avg"]
        operator = ["Comparison"]

        """
        statement = ["Data Manipulation Statement", "SELECT"]
        clause = ["FROM", "WHERE"]
        predicate = []
        expression = []
        operator = ["Comparison", "Conjunction"]
        """

        statement = self.to_lower(statement)
        clause = self.to_lower(clause)
        predicate = self.to_lower(predicate)
        expression = self.to_lower(expression)
        operator = self.to_lower(operator)

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
        query_clause_raw += clause_generate.clause_gen(clause,TABLE)
        query_clause_raw += predicate_generate.predicate_gen(predicate)


        # format the query
        for col_type in col_types:
            for x in query_column_generation.generate_column_options(table_columns):
                query_statement = query_statement_raw
                query_statement += x
                query_statement += expression_generate.expression_gen(expression,int_cols,string_cols)
                rules = operator_generate.operator_gen(operator)
                for y in query_clause_generation.generate_clause(column_split, col_type, rules):
                    query_clause = query_clause_raw
                    query_clause += y
                    query_formatted = query_statement + ' ' + query_clause
                    yield query_formatted

    @staticmethod
    def to_lower(list):
        return [item.lower() for item in list]

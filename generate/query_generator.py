from query_clause_generation import generate_clause
from query_column_generation import generate_column_options
import os
import sys


class QueryGenerator:
    class QueryLogger:
        def __init__(self):
            self.__query_count=0
            self.__queries=[]
        def add_query(self,query):
            if self.__query_count == 5:
                return
            self.__query_count+=1
            self.__queries.append(query)
        def get_queries(self):
            return self.__queries
        def reset(self):
            self.__queries=[]
        def toString(self):
            for x in self.__queries:
                print(x)

    def __init__(self,debug=None):
        self.debug=debug
        if self.debug:
            self.generator_logger = self.QueryLogger()
            from common import randop, base_test
            basedir = os.path.realpath(os.path.dirname(__file__))
            sys.path.append(os.path.join(basedir, "..", ".."))
            configPath = os.path.realpath(os.path.join(os.pardir, "test.conf-sample"))
            dbs = ["oracle", "target"]
            test_obj = base_test.BaseTest(configPath, dbs)
            test_obj.setup_connections()
            test_obj.get_table_names()
            test_obj.drop_tables()
            test_obj.build_test_tables()
            test_obj.get_table_cols()
            table_columns = test_obj.table_cols
            table_column_types = test_obj.table_col_types
            self.setup("CORP",table_columns,table_column_types)

    def setup(self,table_name, cols, col_types):
        self.table_name=table_name
        self.table_columns=cols
        self.table_column_types=col_types
        self.string_cols=[self.table_columns[0][i] for i in range(len(self.table_column_types[0]))
                       if self.table_column_types[0][i] == 1043]
        self.int_cols=[self.table_columns[0][i] for i in range(len(self.table_column_types[0]))
                    if self.table_column_types[0][i] == 23]
        self.column_split=[self.string_cols,self.int_cols]
        self.set_dictionaries()

    def walk_dict(self,dict,clauses=[]):
        for value in dict:
            if isinstance(dict, set):
                clauses.append(value)
            elif dict[value]:
                self.walk_dict(dict[value], clauses)
        return clauses

    def set_dictionaries(self):
        self.statement_dict = \
                        {'dms':
                            {'select':
                                {'SELECT'}
                            }
                        }

        self.clause_dict = \
                    {'from':
                        {'where':
                            {'FROM {} WHERE'}
                        },
                    'aggregate':
                        {'from':
                            {'orderby':
                                {'group by {}',
                                    'group by {} where'
                                }
                            }
                        }
                    }
        self.operator_dict=\
                    {'comparison':
                         {'=', '>', '<', '<=', '>=', '!='}
                    }

        # supported generations
        # based off of the CORP table in generate_tables.py
        self.supported_dict={
            1:'SELECT {0} FROM {1} WHERE {2}',
            2:'SELECT {0}, {1}({2}) FROM {3} GROUP BY {0}',
            3:'SELECT {0}, {1}({2}) as age FROM {3} GROUP BY {0} HAVING age > 3.0'
        }

    def get_queries(self,test_file=None):
        col_types = ["VarChar", "Int"]
        generation = 2
        col = "AVG"
        operator_key='comparison'
        self.get_queries_setup(generation,col)

        # go through the column types
        for col_type in col_types:
            for col_option in generate_column_options(self.table_columns):
                rules = list(self.operator_dict[operator_key])
                for clause_expression in generate_clause(self.column_split, col_type, rules):
                    query=self.get_queries_helper(generation,col_option,self.table_name,clause_expression)
                    if self.debug and query is not None:
                        self.generator_logger.add_query(query)

    def get_queries_setup(self,generation,col=None):
        if generation == 1:
            pass
        elif generation == 2:
            # this is the col that the aggregation is going to be performed on
            self.col_indicator=self.int_cols[0]
            self.agg_function=col

    def get_queries_helper(self,generation,col_option,table_name,clause_expression):
        query=None
        if generation == 1:
            query = self.supported_dict[generation].format(col_option, table_name, clause_expression)
        elif generation == 2:
            if not ('*' in col_option) and not (self.col_indicator in col_option):
                query = self.supported_dict[generation]\
                    .format(col_option, self.agg_function,self.col_indicator,table_name)
        elif generation == 3:
            pass
        return query



"""
z = QueryGenerator(True)
z.get_queries()
z.generator_logger.toString()
"""

# -*- coding: utf-8 -*-

import os
import sys
import logging
import sqlalchemy

from basetest import LOG

# ==================================================================

SQL_TYPES = {
    "STRING": {
        "CHAR": sqlalchemy.types.String,
        "VARCHAR": sqlalchemy.types.String,
        "TEXT": sqlalchemy.types.Text,
        "VARBINARY": None,
    },
    "NUMERIC": {
        "TINYINT": None,
        "SMALLINT": None,
        "MEDIUMINT": None,
        "INT": sqlalchemy.types.Integer,
        "BIGINT": sqlalchemy.types.BigInteger,
    },
    "DECIMAL": {
        "DECIMAL": None,
        "NUMERIC": sqlalchemy.types.Numeric,
        "REAL": None,
        "FLOAT": sqlalchemy.types.Float,
    },
    "TIMESTAMP": {
        "TIMESTAMP": None,
        "TIME": sqlalchemy.types.Time,
        "DATE": sqlalchemy.types.Date,
        "DATETIME": sqlalchemy.types.DateTime,
    },
    "MISC": {
        "BOOLEAN": sqlalchemy.types.Boolean,
    }
}
ALL_TYPES = []
ALL_TYPES_MAPPINGS = {}
for category in SQL_TYPES:
    for x, y in SQL_TYPES[category].items():
        varName = "TYPE_%s" % x
        globals()[varName] = x
        ALL_TYPES_MAPPINGS[x] = y
        if not y is None: ALL_TYPES.append(x)


## FOR

# ==================================================================


class Table():
    def __init__(self, table_name, conn):
        def get_conn(): return conn

        engine = sqlalchemy.create_engine('postgresql+psycopg2://', creator=get_conn)

        self.engine = engine
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.tableName = table_name
        self.table = sqlalchemy.Table(self.tableName, self.metadata)
        self.attributeCtr = 0
        self.constraintCtr = 0

    ## DEF

    def __next_attr_name(self):
        self.attributeCtr += 1
        return "attr_%02d" % self.attributeCtr

    def __next_constraint_name(self):
        self.constraintCtr += 1
        return "const_%s_%02d" % (self.tableName, self.constraintCtr)

    def add_attribute(self, attr_type, primary_key=False, attr_length=None, attr_null=True, attr_unique=False):
        if not attr_type in ALL_TYPES:
            raise Exception("Unknown type '%s'" % attr_type)
        if ALL_TYPES_MAPPINGS[attr_type] is None:
            raise Exception("Unsupported type '%s'" % attr_type)

        attr_name = self.__next_attr_name()
        target_attr_type = "sqlalchemy.sql.sqltypes.%s" % ALL_TYPES_MAPPINGS[attr_type].__name__
        target_attr_type += "()" if attr_length is None else "(%d)" % attr_length
        attr_type = eval(target_attr_type)

        attr = sqlalchemy.Column(attr_name, attr_type,
                                 primary_key=primary_key,
                                 nullable=attr_null,
                                 unique=attr_unique)
        self.table.append_column(attr)
        LOG.debug("Added attribute %s" % attr)
        return attr_name

    ## DEF

    def add_unique_constraint(self, *attr_names):
        constraint_name = self.__next_constraint_name()
        LOG.debug("Added unique constraint %s %s" % (constraint_name, str(attr_names)))
        const = sqlalchemy.UniqueConstraint(*attr_names, name=constraint_name)
        self.table.append_constraint(const)
        return constraint_name

    ## DEF

    def create(self):
        assert self.table is not None
        LOG.debug("Creating table '%s'" % self.tableName)
        if self.table.exists():
            self.table.drop(checkfirst=False)
        self.table.create()
        ## DEF

## CLASS

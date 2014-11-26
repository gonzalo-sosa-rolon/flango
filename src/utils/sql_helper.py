from django.db import models
from utils import django_util

def add_field(table, column, field_type):
    return "ALTER TABLE {0} ADD COLUMN {1} {2}".format(table, column, field_type)


def drop_field(cls, field):
    
    field_db_name = django_util.get_db_name(field)
    db_table = django_util.get_db_table(cls)
    
    return "ALTER {0} DROP COLUMN {1}".format(db_table, field_db_name)

def create_table(db_table):
    return "CREATE TABLE {0} (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)".format(db_table)

def get_sql_type(field):
    
    if (type(field) is str):
        if field == "TextField":
            return "VARCHAR(250)"
        if field == "DecimalField":
            return "DOUBLE"
        if field == "IntegerField":
            return "INT"
        if field == "ForeignKey":
            return "INT" # TODO add foreing key restriction
        if field == "DateField":
            return "DATE"
        if field == "DateTimeField":
            return "DATETIME"
    else:
        if type(field) is models.TextField:
            return "VARCHAR(250)"
        elif (type(field)) is models.DecimalField:
            return "DOUBLE"
        elif (type(field)) is models.IntegerField:
            return "INT"
        elif (type(field)) is models.ForeignKey:
            return "INT" # TODO add foreing key restriction
        elif (type(field)) is models.DateField:
            return "DATE"
        elif (type(field)) is models.DateTimeField:
            return "DATETIME"
from django.db import models

def get_db_table(cls_or_instance):
    return cls_or_instance._meta.db_table

def get_db_name(field):
    if (field.db_column):
        return field.db_column
    return field.column

def get_field(cls_or_instance, field_name):
    
    for field in get_fields(cls_or_instance):
        if (field_name == get_field_name(field)):
            return field
        
    raise Exception("Field [%s] not found at class [%s]" % (field_name, cls_or_instance))
     
def get_fields(cls_or_instance):
    return cls_or_instance._meta.fields

def get_field_name(field):
    return field.name

def get_field_title(field):
    return field.verbose_name.title()

def is_primary_key(field):
    return field.primary_key
    
def is_foreing_key(field):
    return type(field) == models.ForeignKey
    
def get_value(instance, field):
    if (not is_foreing_key(field)):
        return instance.__dict__[get_field_name(field)]
    else:
        return instance.__dict__[get_field_name(field) + "_id"]
    
def get_field_type_title(field):
    if (type(field) is str):
        if field == "TextField":
            return "Text"
        if field == "DecimalField":
            return "Double"
        if field == "IntegerField":
            return "Integer"
        if field == "ForeignKey":
            return "Foreign key" # TODO add foreing key restriction
        if field == "DateField":
            return "Date"
        if field == "DateTimeField":
            return "Datetime"
    else:
        if type(field) is models.TextField:
            return "Text"
        elif (type(field)) is models.DecimalField:
            return "Double"
        elif (type(field)) is models.IntegerField:
            return "Integer"
        elif (type(field)) is models.ForeignKey:
            return "Foreign Key" # TODO add foreing key restriction
        elif (type(field)) is models.DateField:
            return "Date"
        elif (type(field)) is models.DateTimeField:
            return "Datetime"
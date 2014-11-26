from django.db import models

def get_class(class_name):
    from flango_backend.models import Object, ObjectField
    class_name = str(class_name)
    
    if (class_name.upper() == "OBJECT"):
        return Object
    
    if (class_name.upper() == "OBJECTFIELD"):
        return ObjectField
    
    fields = get_fields(class_name)
    
    module = ''
    
    class Meta():
        app_label = 'flango_backend'
    
    attrs = {'__module__': module, 'Meta': Meta}
    
    for k, v in fields.items():
        attrs[k] = v
        
    result = type(class_name, (models.Model,), attrs)
    globals()[class_name] = result 
    return result
    

def get_fields(class_name):
    from flango_backend.models import ObjectField
    fields = {}
    
    field_objects = ObjectField.objects.filter(field_object__class_name=class_name)
    
    for f in field_objects:
        fields[f.field_name] = get_type(f.field_type, f.field_aditional_info)
        
    return fields

def get_types():
    return ["CharField", "TextField", "ForeignKey", "DecimalField", "IntegerField"]

def get_type(field_type, field_aditional_info):
    from flango_backend.models import ComboField
    
    if (field_type == "CharField"):
        return models.CharField(max_length=255)
    elif (field_type == "TextField"):
        return models.TextField()
    elif (field_type == "ForeignKey"):
        return models.ForeignKey(field_aditional_info)
    elif (field_type == "DecimalField"):
        return models.DecimalField(max_digits=9, decimal_places=2)
    elif (field_type == "IntegerField"):
        return models.IntegerField()
    elif (field_type == "ComboField"):
        return ComboField(field_aditional_info.split(","))

def get_form(class_name):
    
    class_name = str(class_name)
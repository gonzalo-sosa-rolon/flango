from django.db import models
from utils import sql_helper, django_util
from django.db import connection
from flango_backend import models_factory

class Object(models.Model):
    
    class_name = models.TextField()
    plural = models.TextField()
    singular = models.TextField()
    class_name__updateable = False
    
    def save(self, *args, **kwargs):
        
        if (not self.pk):
            cursor = connection.cursor()
            cursor.execute(sql_helper.create_table("flango_backend_" + self.class_name))
        super(Object, self).save(*args, **kwargs)
        

class ComboField(models.TextField):
    
    def __init__(self, values):
        self.values = values
        super(ComboField, self).__init__()

class ObjectField(models.Model):
    field_object = models.ForeignKey('Object')
    field_name = models.TextField()
    field_type = models.TextField()
    mandatory = models.BooleanField()
    field_aditional_info = models.TextField()
    
    field_name__updateable = False
    field_type__updateable = False
    
    def save(self, *args, **kwargs):
        table = "flango_backend_" + self.field_object.class_name
        column = self.get_sql_column()
        field_type = sql_helper.get_sql_type(self.field_type)  
        sql_field = sql_helper.add_field(table, column, field_type)
        if (not self.pk):
            cursor = connection.cursor()
            cursor.execute(sql_field)
        
        super(ObjectField, self).save(*args, **kwargs)
    
    def get_sql_column(self):
        
        if (self.field_type == "ForeignKey"):
            return self.field_name + "_id"
        
        return self.field_name
    
class ObjectForm(models.Model):
    form_name = models.TextField()
    form_class = models.TextField()
    
    @classmethod
    def get_default_form(cls, cls_name):
        return ObjectForm(form_name=cls_name, form_class=cls_name)
     
class ObjectFormField(models.Model):
    field_name = models.TextField()
    posicion = models.IntegerField()
    form = models.ForeignKey("ObjectForm")
    updateable = models.BooleanField(default=True)
    
    @classmethod
    def get_default_fields(cls, obj_form):
        result = []
        form_class = models_factory.get_class(obj_form.form_class)
        
        for i, field in enumerate(django_util.get_fields(form_class)):
            field_name = django_util.get_field_name(field)
            
            if (hasattr(form_class, field_name + "__updateable")):
                updateable = getattr(form_class, field_name + "__updateable")
            else:
                updateable = True
                
            ob_form_field = ObjectFormField(field_name=field_name, form=obj_form, posicion=i, updateable=updateable)
            
            result.append(ob_form_field)
            
        return result
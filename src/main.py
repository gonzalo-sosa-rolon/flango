from flango_backend.models import Object, ObjectField, ObjectForm, \
    ObjectFormField
from flango_backend.models_factory import get_class
from utils import django_util
from utils import sql_helper


if __name__ == "__main4__":
    
    field = django_util.get_field(Object, "class_name")
    django_util.get_db_name(field)
    django_util.get_db_table(Object)
    print (sql_helper.add_field(Object, field))
    print (sql_helper.create_table("Object"))
    
if __name__ == "__main__":
    
    print ("load starting")
    # load classes
    ob = Object()
    
    ob.class_name = "company"
    ob.plural = "Companies"
    ob.singular = "Company"
    
    ob.save()
    
    ob_field = ObjectField()
    
    ob_field.field_name = 'name'
    ob_field.field_type = "TextField"
    ob_field.field_object = ob
    ob_field.mandatory = True
    ob_field.save()
    
    ob_field = ObjectField()
    
    ob_field.field_name = 'address'
    ob_field.field_type = "TextField"
    ob_field.mandatory = True
    ob_field.field_object = ob
    ob_field.save()
    
    ob = Object()
    
    ob.class_name = "employee"
    ob.plural = "Employees"
    ob.singular = "employee"
    
    ob.save()
    
    ob_field = ObjectField()
    
    ob_field.field_name = 'company'
    ob_field.field_type = "ForeignKey"
    ob_field.mandatory = True
    ob_field.field_object = ob
    ob_field.field_aditional_info = 'company'
     
    ob_field.save()
    
    ob_field = ObjectField()
    
    ob_field.field_name = 'first_name'
    ob_field.field_type = "TextField"
    ob_field.mandatory = True
    ob_field.field_object = ob
    ob_field.save()
    
    ob_field = ObjectField()
    
    ob_field.field_name = 'age'
    ob_field.field_type = "DecimalField"
    ob_field.mandatory = True
    ob_field.field_object = ob
    ob_field.save()

    # load registers
    
    Company = get_class("company")
    Employee = get_class("employee")
    
    for i in range(1, 10):
        company = Company()
        company.name = "Company %s " % i
        company.address = "Address %s " % i
        
        company.save()
        
        for j in range(1, 20):
            
            emp = Employee()
            emp.first_name = "Employee %s" % (j * i + j)
            emp.company = company
            emp.age = j * i + j
            
            emp.save()
            
    # load forms
    
    form = ObjectForm()
    form.form_class = "company"
    form.form_name = "company"
    
    form.save()
    
    form_field = ObjectFormField()
    form_field.field_name = "address"
    form_field.posicion = 0
    form_field.form = form
    
    form_field.save()
    
    form_field = ObjectFormField()
    form_field.field_name = "name"
    form_field.posicion = 1
    form_field.form = form
    
    form_field.save()
    
    form = ObjectForm()
    form.form_class = "employee"
    form.form_name = "employee"
    
    form.save()
    
    form_field = ObjectFormField()
    form_field.field_name = "first_name"
    form_field.posicion = 0
    form_field.form = form
    
    form_field.save()
    
    form_field = ObjectFormField()
    form_field.field_name = "company"
    form_field.posicion = 1
    form_field.form = form
    
    form_field.save()
    
    form_field = ObjectFormField()
    form_field.field_name = "age"
    form_field.posicion = 2
    form_field.form = form
    
    form_field.save()
    
    print ("load finished successfully")
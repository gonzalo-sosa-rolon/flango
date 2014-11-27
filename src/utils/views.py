from decimal import Decimal
from django.db import models
from django.db.models.fields import TextField
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from flango_backend.models import ObjectField, ObjectForm, ObjectFormField, \
    Object
from flango_backend.models_factory import get_class
from utils import django_util
import json


class FlangoTemplateView(TemplateView):
    
    def get_objects(self):
        result = []
        
        for obj in Object.objects.all():
            result.append({"label": str(obj.plural), 
                           "link": "/list/" + (obj.class_name)})
        return result

class ListView(FlangoTemplateView):
    template_name = "flango_list.html"
    rows = 20
    
    def get_class(self):
        return get_class(self.args['cls'])
    
    def get_title(self):
        return self.args['cls'].title()
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        self.args = kwargs
        page = 0
        
        if ('page' in kwargs):
            try:
                page = int(kwargs['page'])
            except:
                page = 1
        else:
            page = 1
                
        context["title"] = self.get_title()
        context["fields"] = self.__get_fields()
        context["elements"] = self.__get_elements(page)
        context["objects"] = self.get_objects()
        context["pages"] = self.__get_pages(page)
        
        return context
    
    def __get_order_by(self):
        
        if (self.request.GET):
            if ("sort__field" in self.request.GET):
                try:
                    return str(self.request.GET["sort__field"])
                except:
                    return False
            return False
            
    def __prepare_filters(self):
        filters = {}
        
        if (self.request.GET):
            for field in django_util.get_fields(self.get_class()):
                
                fieldname = django_util.get_field_name(field)
                
                if (fieldname in self.request.GET):
                    
                    if (type(field)) is TextField:    
                        filters[fieldname + "__contains"] = self.request.GET[fieldname]
                    elif (type(field)) is models.DecimalField:
                        filters[fieldname] = Decimal(self.request.GET[fieldname])
                    elif (type(field)) is models.IntegerField:
                        filters[fieldname] = self.request.GET[fieldname]
                    elif (type(field)) is models.ForeignKey:
                        filters[fieldname + "_id"] = int(self.request.GET[fieldname])
                    else:
                        filters[fieldname] = self.request.GET[fieldname]
                        
        return filters
    
    def __get_pages(self, page):
        result = []
        
        filters = self.__prepare_filters()
        
        if (not filters):
            count = self.get_class().objects.all().count()
        else:
            count = self.get_class().objects.filter(**filters).count()
            
        count_of_pages = (count / self.rows) + 1
        
        if (count_of_pages < 25):
            for page_number in range(1, count_of_pages):
                result.append(self.create_page_link(page_number, page))
        else:
            if (page < 12):
                for page_number in range(1, page):
                    result.append(self.create_page_link(page_number, page))
                
                for page_number in range(page, 25):
                    result.append(self.create_page_link(page_number, page))
                
                result.append(self.create_page_link((page + count_of_pages) // 2, page, "..."))
                result.append(self.create_page_link(count_of_pages, page))
            elif (page + 12 > count_of_pages):
                
                result.append(self.create_page_link(1, page))
                result.append(self.create_page_link((page + 1) / 2, page, '...'))
                
                for page_number in range(count_of_pages + (count_of_pages - page) - 25, count_of_pages + 1):
                    result.append(self.create_page_link(page_number, page))
            else:
                result.append(self.create_page_link(1, page))
                result.append(self.create_page_link((1 + page) / 2, page, '...'))
                
                for page_number in range(page - 12, page + 12):
                    result.append(self.create_page_link(page_number, page))
                
                result.append(self.create_page_link((page + count_of_pages) // 2, page, '...'))
                
                    
                result.append(self.create_page_link(count_of_pages, page))
                
        return result
        
    def create_page_link(self, page_number, page, label=''):
        
        if not label:
            label = page_number
        
        parameters = []
        
        for parameter in self.request.GET:
            parameters.append(parameter + "=" + self.request.GET[parameter])
        
        parameters_str = "?" + "&".join(parameters)
        
        return {'link': '/employees/%d/%s' % (page_number, parameters_str),  
                'label': label, 'is_current_page': page_number == page}
        
    def __get_elements(self, page):
        
        result = []
        filters = self.__prepare_filters()
        
        order_by = self.__get_order_by()
        if (not filters):
            if (order_by):
                elements = self.get_class().objects.order_by(order_by).all()[(page - 1) * self.rows:page * self.rows]
            else:
                elements = self.get_class().objects.all()[(page - 1) * self.rows:page * self.rows]
        else:
            if (order_by):
                elements = self.get_class().objects.filter(**filters).order_by(order_by)[(page - 1) * self.rows:page * self.rows]
            else:
                elements = self.get_class().objects.filter(**filters)[(page - 1) * self.rows:page * self.rows]
        
        for element in elements:
            element_data = []
            
            for field in django_util.get_fields(self.get_class()):
                element_data.append(django_util.get_value(element, field))
                
            result.append(element_data)
            
        return result
            
    def __is_order_asc(self, field):
        order = self.__get_order_by()
    
        if (order): 
            return field == order
        
    def __is_order_desc(self, field):
        order = self.__get_order_by()
    
        if (order): 
            return field == order[1:] #remove - character
    
    def __get_fields(self):
        
        result = []
        
        for field in django_util.get_fields(self.get_class()):
            field_name = django_util.get_field_name(field)
            field_description = {'title': django_util.get_field_title(field),
                                 'name': field_name,
                                 'asc': self.__is_order_asc(field_name),
                                 'desc': self.__is_order_desc(field_name)}
            
            result.append(field_description)
            
        return result


class FLangoNewObject(FlangoTemplateView):
    template_name = "flango_new_object.html"
        
class FLangoObjectsSettings(FlangoTemplateView):
    
    template_name = "flango_objects_settings.html"
    
    def get_context_data(self, **kwargs):
        context = super(FLangoObjectsSettings, self).get_context_data(**kwargs)
        
        context["objects"] = self.get_objects()
        context["existing_objects"] = list(Object.objects.all())
        return context
    
class FormView(FlangoTemplateView):
    
    template_name = "flango_form.html"
    
    def post(self, request, *args, **kwargs):
        
        response_data = {'error': 0, 'data': 'SUCCESS'}
        
        try:
            cls = get_class(kwargs['cls'])
            data = {}
            for field in django_util.get_fields(cls):
                field_name = django_util.get_field_name(field)

                if (django_util.is_primary_key(field)):
                    if (field_name in self.request.POST and not self.request.POST[field_name]):
                        continue

                if (field_name in self.request.POST):
                    data[field_name] = self.request.POST[field_name]
            
            instance = cls(**data)
            instance.save()
                    
        except Exception as e:
            response_data['error'] = 1
            response_data['data'] = str(e)
                        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    def get_class(self, cls=""):
        
        if (not cls):
            cls = self.args['cls']
            
        return get_class(cls)
    
    def get_title(self):
        return self.args['cls'].title()
    
    def get_field_input(self, field, value="", updateable=True):
        name = django_util.get_field_name(field)
        title = django_util.get_field_title(field)
        
        if (django_util.is_primary_key(field) or not updateable):
            return'<input type="TEXT" name="%s" value="%s" class="form-control" placeholder="%s" readonly/>' % (name, value, title)
        else:
            return'<input type="TEXT" id="%s" name="%s" value="%s" class="form-control" placeholder="%s"/>' % (name, name, value, title)
        
    def get_form(self, cls=""):
        
        if not cls:
            cls = self.args['cls']
            
        try:
            ob_form = ObjectForm.objects.get(form_name=str(cls))
            fields = ObjectFormField.objects.filter(form=ob_form).order_by('posicion')
        except:
            print ("Getting default form for class")
            ob_form = ObjectForm.get_default_form(cls)
            fields = ObjectFormField.get_default_fields(ob_form)
        form = []
        cls = self.get_class(cls)
        instance = None
        
        if ('pk' in self.args):
            instance = cls.objects.get(pk=self.args['pk'])
            
        for f in fields:
            field = django_util.get_field(cls, f.field_name)
            value = ''
            updateable = True
            
            if (instance is not None):
                value = django_util.get_value(instance, field)
                updateable = f.updateable
            field_type = django_util.get_field_type_title(field)
            form.append({'title': django_util.get_field_title(field),
                         'name': f.field_name,
                         'type': field_type,
                         'pk': f.pk,
                         'input': self.get_field_input(field, value, updateable)})
            
            
        return form
        
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        self.args = kwargs
        
        context["title"] = self.get_title()
        context["objects"] = self.get_objects()
        context['form'] = self.get_form()
        
        return context
    
class FLangoEditObject(FlangoTemplateView):
    template_name = "flango_edit_object.html"
    
    def get_title(self):
        return self.args['cls'].title()
    
    def get_fields(self):
        result = []
        fields = ObjectField.objects.filter(field_object__class_name__contains=str(self.class_name))
        
        for f in fields:
            result.append({'field_name': f.field_name,
                          'field_type': f.field_type,
                          'mandatory': f.mandatory})
        return result
    
    def get_field_input(self, field, value="", updateable=True):
        name = django_util.get_field_name(field)
        title = django_util.get_field_title(field)
        
        if (django_util.is_primary_key(field) or not updateable):
            return'<input type="TEXT" name="%s" value="%s" class="form-control" placeholder="%s" readonly/>' % (name, value, title)
        else:
            return'<input type="TEXT" id="%s" name="%s" value="%s" class="form-control" placeholder="%s"/>' % (name, name, value, title)
        
    def get_form(self):
        
        cls = "Object"
            
        try:
            ob_form = ObjectForm.objects.get(form_name=cls)
            fields = ObjectFormField.objects.filter(form=ob_form).order_by('posicion')
        except:
            print ("Getting default form for class")
            ob_form = ObjectForm.get_default_form(cls)
            fields = ObjectFormField.get_default_fields(ob_form)
            
        form = []
        cls = get_class(cls)
        instance = None
        
        instance = cls.objects.get(pk=self.pk)
            
        for f in fields:
            field = django_util.get_field(cls, f.field_name)
            value = ''
            updateable = True
            
            if (instance is not None):
                value = django_util.get_value(instance, field)
                updateable = f.updateable
            field_type = django_util.get_field_type_title(field)
            form.append({'title': django_util.get_field_title(field),
                         'name': f.field_name,
                         'type': field_type,
                         'pk': f.pk,
                         'input': self.get_field_input(field, value, updateable)})
            
        return form
            
    def get_context_data(self, **kwargs):
        self.pk = int(kwargs['pk'])
        self.obj_to_edit = Object.objects.get(pk=self.pk)
        self.class_name = str(self.obj_to_edit.class_name)
        context = super(FLangoEditObject, self).get_context_data(**kwargs)
        self.args = kwargs
        context['class_fields'] = self.get_fields()
        context['title'] = self.class_name
        context["objects"] = self.get_objects()
        context["form"] = self.get_form()
        
        return context

        
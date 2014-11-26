from django.conf.urls import patterns, include, url
from test_models.views import EmployeeList
from utils.views import ListView, FormView, FLangoObjectsSettings, FLangoNewObject, FLangoEditObject


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flango.views.home', name='home'),
    # url(r'^flango/', include('flango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url('^employees/$', EmployeeList.as_view()),
    url('^employees/(?P<page>\d+)/$', EmployeeList.as_view()),
    url('^list/(?P<cls>\w+)/$', ListView.as_view()),
    url('^list/(?P<cls>\w+)/(?P<page>\d+)/$', ListView.as_view()),
    url('^form/(?P<cls>\w+)/$', FormView.as_view()),
    url('^form/(?P<cls>\w+)/(?P<pk>\d+)/$', FormView.as_view()),
    url('flango/objects/$', FLangoObjectsSettings.as_view()),
    url('^flango/objects/edit/(?P<pk>\d+)/$', FLangoEditObject.as_view()),
)

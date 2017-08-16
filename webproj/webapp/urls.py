from django.conf.urls import url
from django.views.generic import ListView, DetailView
from . import views
from . models import Info


urlpatterns = [
    url(r'^$', views.index, name="index"),

    url(r'^contact/$', views.contact, name="contact"),

    # look at modelname.objects.all() -> object_list is the variable in data.html
    url(r'^data/$', ListView.as_view(queryset=Info.objects.all().order_by("-date")[:25], template_name="webapp/data.html")),

    #the name of the variable must be small letters as that of model name
    url(r'^data/(?P<pk>\d+)/$', DetailView.as_view(model=Info,template_name="webapp/entry.html")),

    #list data passing to javascript for d3 rendering
    url(r'^layout-ex/$', views.layout_ex, name="layout_ex"),

    #serialized data passing to javascript for d3 rendering
    url(r'^layout-cells/$', views.layout_cells, name="layout_cells"),

    #serialized data passing to javascript for d3 rendering
    url(r'^layout-dept/$', views.layout_dept, name="layout_dept"),

    #search for a department and treemap plot cells in it
    url(r'dept-cells/$', views.dept_cells, name="dept-cells"),

    #search for departments to be connected
    url(r'dept-dept/$', views.dept_dept, name="dept-dept"),
]

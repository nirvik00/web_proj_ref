from django.conf.urls import url
from django.views.generic import ListView, DetailView
from . import views
from . models import Info


urlpatterns = [

    url(r'^$', views.home, name="index"),

    url(r'^contact/$', views.contact, name="contact"),

    #contacts
    url(r'^contact/$', views.contact ,name='contact'),

    #display data
    url(r'^data/$', views.display_data, name='display_data'),

    #list data passing to javascript for d3 rendering
    url(r'^layout-ex/$', views.layout_ex, name="layout_ex"),

    #serialized data passing to javascript for d3 rendering
    url(r'^layout-cells/$', views.layout_cells, name="layout_cells"),

    #serialized data passing to javascript for d3 rendering
    url(r'^layout-dept/$', views.layout_dept, name="layout_dept"),

    #search for a department and treemap plot cells in it
    url(r'^dept-cells/$', views.dept_cells, name="dept-cells-treemap"),

    #treemap layout of departments to be connected
    url(r'^dept-dept/$', views.dept_dept, name="dept-dept-treemap"),

    # complete treemap layout of all cells
    url(r'^cells/$', views.cells_treemap, name="cells_treemap"),

    # search & generate treemap & force layout of departments
    url(r'^flo-dept/$', views.se_dept, name="select_dept"),

    # search & generate treemap & force layout of departments
    url(r'^flo-cells/$', views.se_dept_cells, name="se_dept_cells"),
]

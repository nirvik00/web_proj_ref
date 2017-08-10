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
    url(r'^print/$', views.print, name="print")
]

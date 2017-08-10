import os

from django.shortcuts import render
from django.http import HttpResponse
from .models import Info
from . import plotGraph


def index(request):
    return render(request, "webapp/home.html")

def contact(request):
    return render(request, "webapp/contact.html")

def print(request):
    data=Info.objects.all()
    v=''
    for d in data:
        v+=(d.fname)
    rel_li=plotGraph.read_local()
    return render(request,"webapp/py_db_js.html",{'data0':rel_li})

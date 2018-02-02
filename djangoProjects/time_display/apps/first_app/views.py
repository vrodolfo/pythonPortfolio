# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime  

# Create your views here.
def index(request):
  context = {
  "date":strftime("%b %d, %Y", gmtime()),
  "time":strftime("%H:%M %p", gmtime())
  }
  return render(request, 'index.html' ,context)


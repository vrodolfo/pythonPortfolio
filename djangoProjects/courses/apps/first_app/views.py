# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import Courses
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def index(request):
	if request.session.get('name')== None:
		request.session['name']=""
	if request.session.get('desc')== None:
		request.session['desc']=""
	return render(request, 'first_app/index.html', {"courses":Courses.objects.all()})

def create(request):
	request.session['name']=request.POST['Coursename']
	request.session['desc']=request.POST['desc']
	
	errors = Courses.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
	else:
		Courses.objects.create(name=request.POST['Coursename'], desc=request.POST['desc'])

	request.session['name']=""
	request.session['desc']=""
	return redirect('/')


def confirm(request, number):
	return render(request, 'first_app/confirmation.html', {"course":Courses.objects.get(id=number)})

def destroy(request, number):
	Courses.objects.get(id=number).delete()
	return redirect('/')

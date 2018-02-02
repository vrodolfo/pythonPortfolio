# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	return render(request, 'first_app/index.html', {"users":User.objects.all()})

def add(request):
	return render(request, 'first_app/add.html')

def create(request):
	User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'])
	return redirect('/users/' + str(User.objects.last().id))

def show(request, number):
	if str(request.method) == 'GET':
		return render(request, 'first_app/user.html', {"user":User.objects.get(id=number)} )
	else:
		temp = User.objects.get(id=number)
		temp.first_name = request.POST['first_name']
		temp.last_name = request.POST['last_name']
		temp.email_address = request.POST['email_address']
		temp.save()
		return redirect('/users/'+str(number))

def edit(request, number):
	return render(request, 'first_app/edit.html', {"user":User.objects.get(id=number)} )

def GoBack(request):
	return redirect('/')

def destroy(request, number):
	User.objects.get(id=number).delete()
	return redirect('/')
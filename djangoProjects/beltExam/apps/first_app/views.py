# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from .models import Trips
from django.core.urlresolvers import reverse
from django.contrib import messages
import bcrypt
import datetime

# Create your views here.
def index(request):
	return redirect('/main')

def main(request):
	if request.session.get('user_id')== None:
		request.session['user_id']=""
	if request.session.get('first_name')== None:
		request.session['first_name']=""
	if request.session.get('username')== None:
		request.session['username']=""
	return render(request, 'first_app/index.html')

def goback(request):
	request.session['first_name']   =""
	request.session['username']    =""
	request.session['user_id']      =""
	request.session.clear()
	return redirect('/main')

def login(request):
	errors = {}

	user = Users.objects.filter(username=str(request.POST['username'])).first()

	if user:
		pw= str(request.POST['password'])
		if not bcrypt.checkpw(pw.encode(), user.password.encode()):
			errors['password'] = "Password does not match!"
	else:
		errors['username'] = "Username not registered!"
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/main')
	else:
		request.session['user_id']   =user.id
		request.session['first_name']=user.first_name
		request.session['username'] =user.username
		return redirect('/travels')

def register(request):
	request.session['first_name']   =request.POST['first_name']
	request.session['username']    =request.POST['username']

	errors = Users.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/main')
	else:
		pw= str(request.POST['password'])
		hashed_pw = bcrypt.hashpw(pw, bcrypt.gensalt())
		user = Users.objects.create(first_name=request.POST['first_name'], username=request.POST['username'], password=hashed_pw)
		#request.session['user_id']=Users.objects.last().id
		request.session['user_id'] = user.id
		return redirect('/travels')


###################################33

def join(request, number):

	#create relation many to many.....
	Trips.objects.get(id=number).user_joining.add(Users.objects.get(id=request.session['user_id']))

	return redirect('/travels/destination/'+number)


def destination(request, number):
	
	context = {
		"trip":Trips.objects.filter(id=number),
		"others":Trips.objects.get(id=number).user_joining.all()
	}

	return render(request, 'first_app/destination.html', context)

def addTrip(request):
	#print "date" +str(datetime.datetime.today()).split()[0]
	context = {
		"date":str(datetime.datetime.today()).split()[0]

	}
	return render(request, 'first_app/add.html', context)

def add(request):
	context = {
		"destination":request.POST['destination'], 
		"description":request.POST['description'], 
		"date_from":request.POST['date_from'], 
		"date_to":request.POST['date_to']
	}

	errors = Trips.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		#return render(request, 'first_app/add.html', context)
		return redirect('/addTrip/')
	else:
		user = Users.objects.get(id=request.session['user_id'])
		#create the trip
		Trips.objects.create(user_trip=user, destination=request.POST['destination'], description=request.POST['description'], date_from=request.POST['date_from'] , date_to=request.POST['date_to'])
		print "fron++++++++++++++: " + str(request.POST['date_from'])
		print "to: " + str(request.POST['date_to'])
		return redirect('/travels/')


def result(request):
	exist = 0
	filtered = []
	othersTrips = Trips.objects.all().exclude(user_trip=Users.objects.get(id=request.session['user_id']))
	joining_trips = Users.objects.get(id=request.session['user_id']).user_joiners.all()
	for i in othersTrips:
		for x in joining_trips:
			if i.id == x.id:
				exist = 1
		if exist == 0:
			filtered.append(i)
		exist = 0


	context = {
		"myTrips":Trips.objects.filter(user_trip=Users.objects.get(id=request.session['user_id'])), 
		#"othersTrips": Trips.objects.filter(user_trip!=Users.objects.get(id=request.session['user_id']))
		"othersTrips": Trips.objects.all().exclude(user_trip=Users.objects.get(id=request.session['user_id'])),
		#"joining_trips":Trips.objects.all().user_joining.filter(id=Users.objects.get(id=request.session['user_id']))
		"joining_trips": Users.objects.get(id=request.session['user_id']).user_joiners.all(),
		"filtered":filtered
		
	}
	return render(request, 'first_app/result.html', context)
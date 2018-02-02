# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(str(postData['first_name'])) < 3:
			errors['first_name'] = "First name should be more than 2 characters"
		if any(map(str.isdigit, str(postData['first_name']))):
			errors['first_name'] = "First name should be letters only"

		if len(str(postData['username'])) < 3:
			errors['username'] = "Username should be more than 2 characters"
		if any(map(str.isdigit, str(postData['username']))):
			errors['username'] = "Username should be letters only"
		duplicate = Users.objects.filter(username=postData['username']).first()
		if duplicate:
			errors['username'] = "Username already exist!"

	
		if len(str(postData['password'])) < 8:
			errors['password'] = "Password should be more than 8 characters"
		elif not any(map(str.isupper, str(postData['password']))):
			errors['password'] = "Password should contain at least 1 Capital Letter"

		
		return errors


class Users(models.Model):
	first_name    = models.CharField(max_length=255)
	username     = models.CharField(max_length=255)
	password      = models.CharField(max_length=255)
	created_at    = models.DateTimeField(auto_now_add = True)
	updated_at    = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __unicode__(self):
		return "id: " + str(self.id) + "first_name: " + str(self.first_name) + ", username: " + str(self.username)



class TripManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}

		if len(str(postData['destination'])) < 2:
			errors['destination'] = "Destination should be more than 2 characters"
		if len(str(postData['description'])) < 2:
			errors['description'] = "description should be more than 2 characters"

		#validate dates
		# if len(str(postData['date_from'])) < 10:
		# 	errors['date_from'] = "date_from should be more than 2 characters"
		# if len(str(postData['date_to'])) < 2:
		# 	errors['date_to'] = "date_from should be more than 2 characters"
		return errors



class Trips(models.Model):
	user_joining  = models.ManyToManyField(Users, related_name="user_joiners")
	user_trip     = models.ForeignKey(Users, related_name = "user_trips")
	destination   = models.CharField(max_length=255)
	description   = models.CharField(max_length=255)
	date_from     = models.DateTimeField()
	date_to		  = models.DateTimeField()
	created_at    = models.DateTimeField(auto_now_add = True)
	updated_at    = models.DateTimeField(auto_now=True)
	objects = TripManager()

	def __unicode__(self):
		return "id: " + str(self.id) + "destination: " + str(self.destination) + ", description: " + str(self.description) + ", date_from: " + str(self.date_from) + ", date_to: " + str(self.date_to) + ", user_trip: " + str(self.user_trip)


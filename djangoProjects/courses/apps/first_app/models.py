# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class CoursesManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(str(postData['Coursename'])) < 5:
			errors['Coursename'] = "Course name should be more than 5 characters"
		if len(postData['desc']) < 15:
			errors['desc'] = "Description should be more than 15 characters"
		return errors



class Courses(models.Model):
	name          = models.CharField(max_length=255)
	desc          = models.CharField(max_length=255)
	created_at    = models.DateTimeField(auto_now_add = True)
	updated_at    = models.DateTimeField(auto_now=True)
	# *************************
    # Connect an instance of BlogManager to our Blog model overwriting
    # the old hidden objects key with a new one with extra properties!!!
	objects = CoursesManager()
	# *************************
	def __unicode__(self):
		return "id: " + str(self.id) + "name: " + str(self.name) + ", desc: " + str(self.desc) +  "created_at: " + str(self.created_at)


"""
models come with a hidden key:
      objects = models.Manager()
we are going to overwrite this!
"""

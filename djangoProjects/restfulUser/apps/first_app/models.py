# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	first_name    = models.CharField(max_length=255)
	last_name     = models.CharField(max_length=255)
	email_address = models.CharField(max_length=255)
	created_at    = models.DateTimeField(auto_now_add = True)
	updated_at    = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return "id: " + str(self.id) + "first_name: " + str(self.first_name) + ", last_name: " + str(self.last_name) + ", email_address: " + self.email_address + "created_at: " + str(self.created_at)


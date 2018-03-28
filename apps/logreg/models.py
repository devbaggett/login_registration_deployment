from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z_ ]+$')

class UserManager(models.Manager):
	def validation(self, postData, error_validation):
		errors = {}
		if error_validation == 'register':
			if len(postData['name']) < 3:
				errors['name'] = "Name must contain at least 3 letters!"
			if not NAME_REGEX.match(postData['name']):
				errors['name'] = "Name cannot be blank and can only contain letters!"
			elif not EMAIL_REGEX.match(postData['email']):
				errors['email'] = "Invalid email!"
			elif User.objects.filter(email=postData['email']):
				errors['email'] = "Email already being used!"
			elif len(postData['pw']) < 9:
				errors['pw'] = "Password must contain more than 8 characters!"
			elif not postData['pw'] == postData['confirm_pw']:
				errors['pw'] = "Both passwords must match!"
		if error_validation == 'login':
			user = User.objects.filter(email=postData['email_login'])
			if not EMAIL_REGEX.match(postData['email_login']):
				errors['email_login'] = "Invalid email"
			elif not User.objects.filter(email=postData['email_login']):
				errors['email_login'] = "No email in system"
				print postData['email_login']
			elif not bcrypt.checkpw(postData['pw_login'].encode(), user[0].pw.encode()):
				errors['pw_login'] = "Invalid login and/or password!"
		return errors

class AppointmentManager(models.Manager):
	def validation(self, postData, error_validation):
		errors = {}
		if error_validation == 'add_appointment':
			if len(postData['task']) < 3:
				errors['task'] = "Appointment must have more than 2 characters!"
			if not postData['date']:
				errors['date'] = "No date entered."
			elif datetime.strptime(postData['date'], '%Y-%m-%d').date() < date.today():
				errors['date'] = "Date must be in the future."
			if not postData['time']:
				errors['time'] = "No time entered."
		if error_validation == 'update_appointment':
			if postData['date']:
				if datetime.strptime(postData['date'], '%Y-%m-%d').date() < date.today():
					errors['date'] = "Date must be in the future."
		return errors

# a user can have many appointments
# an appointment can have one user
# one to many relationship

class User(models.Model):
	name 		= models.CharField(max_length=255)
	email 		= models.CharField(max_length=255)
	dob			= models.DateField(null=True, blank=True)
	pw 			= models.CharField(max_length=255)
	objects 	= UserManager()
	def __unicode__(self):
		return self.name

class Appointment(models.Model):
	desc 		= models.TextField()
	time		= models.TimeField()
	date 		= models.DateField()
	status		= models.CharField(max_length=255)
	user 		= models.ForeignKey(User, related_name="appointments")
	objects		= AppointmentManager()
	def __unicode__(self):
		return self.desc
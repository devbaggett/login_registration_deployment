from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def validation(self, postData, error_validation):
		errors = {}
		if error_validation == 'register':
			if len(postData['first_name']) < 2:
				errors['first_name'] = "First name must contain at least 2 letters!"
			elif not NAME_REGEX.match(postData['first_name']):
				errors['first_name'] = "First name cannot be blank and can only contain letters!"
			elif len(postData['last_name']) < 2:
				errors['last_name'] = "Last name must contain at least 2 letters!"
			elif not NAME_REGEX.match(postData['last_name']):
				errors['last_name'] = "Last name cannot be blank and can only contain letters!"
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
		if error_validation == 'remove_id':
			if not postData['id']:
				errors['id'] = "Invalid ID"
			elif not User.objects.filter(id=postData['id']):
				errors['id'] = "Invalid ID"
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	pw = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __unicode__(self):
		return "Author: " + self.first_name

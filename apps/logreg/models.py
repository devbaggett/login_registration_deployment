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
			if len(postData['name']) < 3:
				errors['name'] = "Name must contain at least 3 letters!"
			if not NAME_REGEX.match(postData['name']):
				errors['name'] = "Name cannot be blank and can only contain letters!"
			elif len(postData['alias']) < 3:
				errors['alias'] = "Alias must contain at least 3 letters!"
			elif not NAME_REGEX.match(postData['alias']):
				errors['alias'] = "Alias cannot be blank and can only contain letters!"
			elif User.objects.filter(alias=postData['alias']):
				errors['alias'] = "Alias already being used!"
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

class WishManager(models.Manager):
	def validation(self, postData):
		errors = {}
		if len(postData['item']) < 3:
			errors['item'] = "Item must contain more than 3 characters!"
		return errors

# user can have many pokes
# a user can poke many people

class User(models.Model):
	name 		= models.CharField(max_length=255)
	alias	 	= models.CharField(max_length=255)
	email 		= models.CharField(max_length=255)
	dob			= models.DateField(null=True, blank=True)
	pw 			= models.CharField(max_length=255)
	objects 	= UserManager()
	def __unicode__(self):
		return self.name

class Poke(models.Model):
	creator 	= models.ForeignKey(User, related_name="pokers")
	recipient	= models.ForeignKey(User, related_name="pokees")
	objects		= WishManager()
	def __unicode__(self):
		return unicode(self.creator)
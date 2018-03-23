from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	if "validate" not in request.session:
		request.session['validate'] = ''
	return render(request, 'logreg/index.html')

def register(request):
	request.session['validate'] = 'registration'
	errors = User.objects.validation(request.POST, 'register')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/')
	else:
		new_user = User.objects.create(
			first_name=request.POST['first_name'],
			last_name=request.POST['last_name'],
			email=request.POST['email'],
			pw=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()))
		request.session['first_name'] = new_user.first_name
	return redirect('/success')

def login(request):
	request.session['validate'] = 'login'
	errors = User.objects.validation(request.POST, 'login')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/')
	login_user = User.objects.get(email=request.POST['email_login'])
	request.session['first_name'] = login_user.first_name
	context = {"users": User.objects.all()}
	return redirect('/success', context)

def success(request):
	if "first_name" not in request.session:
		return redirect('/')
	if request.session['validate'] == 'registration':
		messages.success(request, "Successfully registered!")
	elif request.session['validate'] == 'login':
		messages.success(request, "Successfully logged in!")
	context = {"users": User.objects.all()}
	return render(request, 'logreg/success.html', context)

def remove(request):
	errors = User.objects.validation(request.POST, 'remove_id')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/success')
	else:
		user = User.objects.get(id=request.POST['id'])
		user.delete()
	return redirect('/success')

def logoff(request):
	request.session.clear()
	return redirect('/')



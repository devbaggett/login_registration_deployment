from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from django.contrib import messages
from django.db.models import Count
from operator import itemgetter
from .models import *
import bcrypt

def index(request):
	return render(request, 'logreg/index.html')

def register(request):
	errors = User.objects.validation(request.POST, 'register')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
			return redirect('/')
	else:
		new_user = User.objects.create(
			name		= request.POST['name'],
			alias 		= request.POST['alias'],
			email		= request.POST['email'],
			dob			= request.POST['dob'],
			pw			= bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()))
		request.session['name'] = new_user.name
		request.session['id']	= new_user.id
	return redirect('/pokes')

def login(request):
	errors = User.objects.validation(request.POST, 'login')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/')
	else:
		login_user = User.objects.get(email=request.POST['email_login'])
		request.session['name']	= login_user.name
		request.session['id']	= login_user.id
	return redirect('/pokes')

	

def pokes(request):
	current_user = User.objects.get(id=request.session['id'])
	user = User.objects.annotate(num_pokers=Count('pokees')).filter(id=request.session['id']).first()
	if user:
		pokees = user.pokees.all()
		new_pokees = {}
		for poke in pokees:
			if poke.creator.id not in new_pokees:
				new_pokees[poke.creator.id] = [poke.creator.name, 1]
			else:
				new_pokees[poke.creator.id][1] += 1
		new_pokers = []
		for poke in new_pokees.itervalues():
			new_pokers.append(poke)

	pokelist = []
	pokelist = sorted(new_pokers, key=itemgetter(1))
	print pokelist




	context = {
		"pokelist" : pokelist,
		"new_pokees" : new_pokees,
		"poke_count" : len(new_pokees),
		"pokes_acquired" : Poke.objects.filter(recipient=request.session['id']),
		"users" : User.objects.all().exclude(id=request.session['id'])
	}
	return render(request, 'logreg/pokes.html', context)

def pokeSomeone(request, id):
	current_user = User.objects.get(id=request.session['id'])
	user_being_poked = User.objects.get(id=id)
	
	poke = Poke.objects.create(
		creator 		= current_user,
		recipient		= user_being_poked)
	return redirect('/pokes')

def logout(request):
	request.session.clear()
	return redirect('/')
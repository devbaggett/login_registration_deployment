from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from django.contrib import messages
from django.db.models import Count
from operator import itemgetter
from datetime import date, datetime
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
			email		= request.POST['email'],
			dob			= request.POST['dob'],
			pw			= bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()))
		request.session['name'] = new_user.name
		request.session['id']	= new_user.id
	return redirect('/dashboard')

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
	return redirect('/dashboard')

def dashboard(request):
	if 'id' not in request.session:
		return redirect('/')
	current_user = User.objects.get(id=request.session['id'])
	current_date = date.today()
	user_appointments = current_user.appointments.all()
	context = {
		"current_date" : current_date,
		"today_appointments" : current_user.appointments.filter(date=current_date),
		"user_appointments" : user_appointments.exclude(date=current_date)
	}
	return render(request, 'logreg/dashboard.html', context)

def addAppointment(request):
	errors = Appointment.objects.validation(request.POST, 'add_appointment')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/dashboard')

	task = Appointment.objects.create(
		desc = request.POST['task'],
		date = request.POST['date'],
		time = request.POST['time'],
		user = User.objects.get(id=request.session['id']),
		status = "Pending")

	then = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
	now = date.today()

	return redirect('/dashboard')

def editAppointment(request, id):
	if 'id' not in request.session:
		return redirect('/')
	context = {
		"task" : Appointment.objects.get(id=id)
	}
	return render(request, 'logreg/edit_task.html', context)

def updateAppointment(request, id):
	errors = Appointment.objects.validation(request.POST, 'update_appointment')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/edit/' + id)
	task = Appointment.objects.get(id=id)
	if request.POST['desc']:
		task.desc = request.POST['desc']
	if request.POST['time']:
		task.time = request.POST['time']
	if request.POST['date']:
		task.date = request.POST['date']
	if request.POST['status']:
		task.status = request.POST['status']
	task.save()
	return redirect('/dashboard')


def deleteAppointment(request, id):
	task = Appointment.objects.get(id=id)
	task.delete()
	return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')
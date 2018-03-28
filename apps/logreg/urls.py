from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.dashboard),
	url(r'^add_appointment$', views.addAppointment),
	url(r'^delete/(?P<id>\d+)$', views.deleteAppointment),
	url(r'^edit/(?P<id>\d+)$', views.editAppointment),
	url(r'^updateAppointment/(?P<id>\d+)$', views.updateAppointment),
	url(r'^logout$', views.logout)
]
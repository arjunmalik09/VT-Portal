from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
	url(r'^$', 'Registration.views.home', name='home'),
	url(r'^register/$', 'Registration.views.register', name='register'),
	url(r'^verify/$', 'Registration.views.verify', name='verify'),
 	url(r'^login/$', 'Registration.views.user_login', name='login'),
 	url(r'^logout/$', 'Registration.views.user_logout', name='logout'),	 
 	url(r'^profile/$', 'Registration.views.show_profile', name='show_profile'),	 
 	url(r'^profile/edit/$', 'Registration.views.edit_profile', name='edit_profile'),	 		  
]
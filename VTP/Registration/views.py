from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from random import SystemRandom
from string import ascii_lowercase,digits

from .forms import UserProfileForm,UserForm,ProfileForm
from .models import UserProfile
from django.db import connection


# Create your views here.
def home(request):
	context = {
	    'request': request, 
	    'user': request.user,
	}
	return render(request, 'Registration/home.html', context)

@csrf_exempt
def register(request):
	if request.method == 'POST':
		
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			profile = profile_form.save(commit=False)

			user.username = user.email.split('@')[0]
			profile.id = user.username
			profile.psswd = user.password
			profile.first_name = user.first_name
			profile.last_name = user.last_name
			profile.email = user.email
			
			user.set_password(user.password)
			print "Registering:",user.username," with pwd ",user.password
			user.save()
			profile.save()

			return HttpResponse("Your account has been registered with username:"+user.username+" .<a href='/'>Back To Homepage.</a>")

		else:
			print user_form.errors, profile_form.errors

			context = {
		        'user_form': user_form, 
		        'profile_form': profile_form,
	    	}
			return render(request, 'Registration/register.html',context)
		

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		context = {
	        'user_form': user_form, 
	        'profile_form': profile_form,
    	}
		print context
		return render(request, 'Registration/register.html', context)

def verify(request): 
	#return render(request,'verify.html',{ })
	return HttpResponse("Your account has been verified.")


def user_login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct. If None, no user with matching credentials was found.
        if user:
            if user.is_active:           
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse("Your account has been deactivated.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'Registration/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def show_profile(request):
	profile = UserProfile.objects.raw('select * from user_profile where username = %s',[str(request.user.username)])[0]
	context = {	    
	    'profile': profile,
	}
	return render(request, 'Registration/profile.html', context)

@login_required
def edit_profile(request):
	profile = UserProfile.objects.raw('select * from user_profile where username = %s',[str(request.user.username)])[0]
	user = get_object_or_404(User,username = request.user.username)
	if request.method == 'GET':
	    profile_form = ProfileForm(None,instance=profile)
	else:
	    profile_form = ProfileForm(request.POST,instance=profile)
	    
	    if profile_form.is_valid():
			if profile.psswd==request.POST.get('password'):
				profile = profile_form.save(commit=False)
				user.first_name = profile.first_name
				user.username = profile.username
				user.last_name = profile.last_name
				user.email = profile.email
				user.save()
				profile.save()
				messages.success(request,"Updated",extra_tags="html_safe")
				return redirect('/profile')
			else:
				messages.info(request,"Wrong password.",extra_tags="html_safe")
	context = {
	    'profile_form': profile_form,
	}
	return render(request, 'Registration/profile.html', context)
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

from .forms import PilgrimForm,PilgrimEditForm
from Registration.models import UserProfile
from django.db import connection, transaction, DatabaseError, IntegrityError

from .functions import namedtuplefetchall,dictfetchall,parse
import datetime

@login_required
def create_pilgrim(request):
	if request.method == 'POST':
		# create a form instance and populate with data 
		pilgrim_form = PilgrimForm(request.POST)

		if pilgrim_form.is_valid():
			user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
			aadhar_card_no = pilgrim_form.cleaned_data['aadhar_card_no']
			first_name = pilgrim_form.cleaned_data['first_name']
			last_name = pilgrim_form.cleaned_data['last_name']
			gender = pilgrim_form.cleaned_data['gender']
			dob = pilgrim_form.cleaned_data['dob']

			with connection.cursor() as c:
				try:
					vals = [str(user_aadhar_card_no), str(aadhar_card_no), str(first_name), str(last_name), str(gender), str(dob)]
					c.execute('insert into pilgrim values (%s,%s,%s,%s,%s,%s)',vals)
					#row = cursor.fetchone()
				except IntegrityError:
					print "IntegrityError",str(IntegrityError)
					messages.error(request,"Integrity Error.",extra_tags="html_safe")
				except DatabaseError:
					print "DatabaseError",str(DatabaseError)
					messages.error(request,"Database Error.",extra_tags="html_safe")

		else:
			messages.error(request,"Invalid Details of Pilgrim.",extra_tags="html_safe")
		return redirect('/pilgrim')
	# if a GET, a blank form
	else:
	    pilgrim_form = PilgrimForm()

	return render(request, 'Booking/pilgrim.html', {'form': pilgrim_form})

@login_required
def edit_pilgrim(request,id):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	aadhar_card_no = id
	if request.method == 'POST':
			
		pilgrim_form = PilgrimEditForm(request.POST)
		if pilgrim_form.is_valid():
			first_name = pilgrim_form.cleaned_data['first_name']
			last_name = pilgrim_form.cleaned_data['last_name']
			dob = pilgrim_form.cleaned_data['dob']

			with connection.cursor() as c:
				try:
					vals = [str(first_name), str(last_name), str(dob), str(user_aadhar_card_no), str(aadhar_card_no)]
					c.execute('update pilgrim set first_name = %s, last_name = %s, dob = %s where user_aadhar_card_no = %s and aadhar_card_no = %s',vals)
					messages.success(request,"<a href='/pilgrim'>Pilgrim</a> Updated",extra_tags="html_safe")
				except IntegrityError:
					print "IntegrityError",str(IntegrityError)
					messages.error(request,"Integrity Error.",extra_tags="html_safe")
				except DatabaseError:
					print "DatabaseError",str(DatabaseError)
					messages.error(request,"Database Error.",extra_tags="html_safe")
		else:
			messages.error(request,"Invalid Details of Pilgrim.",extra_tags="html_safe")
		return redirect('/pilgrim')
	# if a GET, a blank form
	else:
		data = []
		with connection.cursor() as c:
				try:
					vals = [str(user_aadhar_card_no), str(aadhar_card_no)]
					#print 'select first_name, last_name,dob from pilgrim where user_aadhar_card_no = %s and aadhar_card_no = %s)',vals
					#print 'select * from pilgrim where user_aadhar_card_no = %s and aadhar_card_no = %s)'%vals
					c.execute('select * from pilgrim where user_aadhar_card_no = %s and aadhar_card_no = %s',vals)
					data = dictfetchall(c)

				except IntegrityError:
					print "IntegrityError",str(IntegrityError)
					messages.error(request,"Integrity Error.",extra_tags="html_safe")
				except DatabaseError:
					print "DatabaseError",DatabaseError.message
					messages.error(request,"Database Error.",extra_tags="html_safe")

		pilgrim_form = PilgrimEditForm(data = data[0])

	return render(request, 'Booking/pilgrim_edit.html', {'form': pilgrim_form,'aadhar_card_no':aadhar_card_no})    

@login_required
def delete_pilgrim(request,id):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	print user_aadhar_card_no," deleted ",id
	list_nt = []
	with connection.cursor() as c:
		try:
			c.execute('delete from pilgrim where user_aadhar_card_no = %s and aadhar_card_no = %s',[user_aadhar_card_no,id])
		except IntegrityError:
			print "IntegrityError",str(IntegrityError)
			messages.error(request,"Integrity Error.",extra_tags="html_safe")
		except DatabaseError:
			print "DatabaseError",str(DatabaseError)
			messages.error(request,"Database Error.",extra_tags="html_safe")

	return redirect('/pilgrim')

@login_required
def pilgrim_list(request):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	list_nt = []
	with connection.cursor() as c:
		try:
			c.execute('select aadhar_card_no, first_name, last_name, gender, dob from pilgrim where user_aadhar_card_no = %s',[user_aadhar_card_no])
			list_nt = namedtuplefetchall(c)
		except IntegrityError:
			print "IntegrityError",str(IntegrityError)
			messages.error(request,"Integrity Error.",extra_tags="html_safe")
		except DatabaseError:
			print "DatabaseError",str(DatabaseError)
			messages.error(request,"Database Error.",extra_tags="html_safe")
	
	return render(request, 'Booking/pilgrim_list.html', {'list': list_nt})

@login_required
def book_darshan(request):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	if request.method == 'POST':

		id = request.POST.get('id')
		book_for_list = request.POST.getlist('book_for')
		book_for_self = request.POST.get('book_for_self')
		# print "id_list:",id," id:",type(id),request.POST.get('id')
		# print "book_for:",book_for_list[0],book_for_list[1]," type:",type(book_for_list)," len:",len(book_for_list)
		# print "book_for_self:",book_for_self," type:",type(book_for_self)
		
		with connection.cursor() as c:
			try:
				if(book_for_self == "self"):
					vals = [ str(user_aadhar_card_no), id, str(datetime.datetime.now())[:19]]
					print "booking self with",vals
					c.execute('insert into books_darshan_self values (%s,%s,%s)',vals)
				for book_for in book_for_list:
					vals = [ str(user_aadhar_card_no), book_for,id, str(datetime.datetime.now())[:19]]
					print "booking pilgrim with",vals
					c.execute('insert into books_darshan values (%s,%s,%s,%s)',vals)
				
			except IntegrityError:
				print "IntegrityError",str(IntegrityError)
				messages.error(request,"Integrity Error.",extra_tags="html_safe")
			except DatabaseError:
				print "DatabaseError",str(DatabaseError)
				messages.error(request,"Database Error.",extra_tags="html_safe")

		return redirect('/')
	# if a GET, a blank form
	else:
		with connection.cursor() as c:
			try:
				val = [str(datetime.date.today())[:-2] +str(int(datetime.date.today().day)+1)]	#date for tommorow
				c.execute('select * from darshan where start_time > %s',val)
				list_nt = namedtuplefetchall(c)
				c.execute('select * from pilgrim where user_aadhar_card_no = %s',[user_aadhar_card_no])
				list_nt2 = namedtuplefetchall(c)
			except IntegrityError:
				print "IntegrityError",str(IntegrityError)
				messages.error(request,"Integrity Error.",extra_tags="html_safe")
			except DatabaseError:
				print "DatabaseError",str(DatabaseError)
				messages.error(request,"Database Error.",extra_tags="html_safe")

	return render(request, 'Booking/book_darshan.html', {'list': list_nt,'list2': list_nt2})


@login_required
def my_darshans(request):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	with connection.cursor() as c:
			try:
				val = [user_aadhar_card_no]	
				c.execute('select bds.darshan_id,bds.user_aadhar_card_no,bds.book_time,d.price,d.start_time,d.end_time from \
					(books_darshan_self as bds inner join darshan as d on bds.darshan_id=d.id) where bds.user_aadhar_card_no = %s \
					  order by bds.book_time desc',val)
				list_nt = namedtuplefetchall(c)
				c.execute('select bd.plgm_aadhar_card_no,bd.book_time,d.price,d.start_time,d.end_time from \
					(books_darshan as bd inner join darshan as d on bd.darshan_id=d.id) where bd.user_aadhar_card_no = %s \
					order by bd.book_time desc',val)
				list_nt2 = namedtuplefetchall(c)
			except IntegrityError:
				print "IntegrityError",str(IntegrityError)
				messages.error(request,"Integrity Error.",extra_tags="html_safe")
			except DatabaseError:
				print "DatabaseError",str(DatabaseError)
				messages.error(request,"Database Error.",extra_tags="html_safe")

	return render(request, 'Booking/my_darshans.html', {'list': list_nt,'list2': list_nt2})

@login_required
def book_room_darshan(request,id):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	print "Room for darshan_id:",id," aadhar:",user_aadhar_card_no

	with connection.cursor() as c:
		try:
			vals = [user_aadhar_card_no,int(id)]
			if c.execute('select * from books_darshan_self where  user_aadhar_card_no = %s and darshan_id = %s', vals) > 0:
				val = [id]	
				c.execute('select start_time from darshan where id = %s',val)
				time = namedtuplefetchall(c)
				date = str(time[0].start_time)[:10]
				print date
				return redirect('book_room',date=date)
			else:
				print "Error"
				messages.error(request,"Error.",extra_tags="html_safe")
		except IntegrityError:
			print "IntegrityError",str(IntegrityError)
			messages.error(request,"Integrity Error.",extra_tags="html_safe")
		except DatabaseError:
			print "DatabaseError",str(DatabaseError)
			messages.error(request,"Database Error.",extra_tags="html_safe")

	return redirect('/')

@login_required
def book_room(request,date=None):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	print "Room for date:",date," aadhar:",user_aadhar_card_no

	if request.method == 'POST':
		if request.POST.get('date'):
			date = request.POST.get('date')
		room_no = request.POST.get('room_no')
		with connection.cursor() as c:
			try:	
				vals = [ str(user_aadhar_card_no), str(room_no),str(datetime.datetime.now())[:19], str(date)]
				print "booking self with",vals
				c.execute('insert into books_accomodation values (%s,%s,%s,%s)',vals)
			
			except IntegrityError:
				print "IntegrityError",str(IntegrityError)
				messages.error(request,"Integrity Error.",extra_tags="html_safe")
			except DatabaseError:
				print "DatabaseError",str(DatabaseError)
				messages.error(request,"Database Error.",extra_tags="html_safe")
		print "done"
		return redirect('/')
	# if a GET, a blank form
	else:
		if request.GET.get('date'):
			date = request.GET.get('date')
		with connection.cursor() as c:
			try:
				list_nt = []
				row_no = c.execute('select * from room where room_no not in (select ba.room_no from \
					books_accomodation ba where ba.for_date = %s) and room_no not in \
					(select ba.room_no from books_accomodation ba where ba.user_aadhar_card_no  = %s)',[date,user_aadhar_card_no])
				if row_no>0:
					list_nt = namedtuplefetchall(c)
				else:
					print "No room availabe"
					messages.error(request,"No room availabe.",extra_tags="html_safe")
					return redirect('/my_bookings/darshan/')

			except IntegrityError:
				print "IntegrityError",str(IntegrityError)
				messages.error(request,"Integrity Error.",extra_tags="html_safe")
			except DatabaseError:
				print "DatabaseError",str(DatabaseError)
				messages.error(request,"Database Error.",extra_tags="html_safe")

	return render(request, 'Booking/book_room.html', {'list': list_nt,'date':date})


@login_required
def my_rooms(request):
	user_aadhar_card_no = get_object_or_404(UserProfile,username=request.user.username).aadhar_card_no
	with connection.cursor() as c:
			try:
				val = [user_aadhar_card_no]	
				c.execute('select * from books_accomodation where user_aadhar_card_no = %s',val)
				list_nt = namedtuplefetchall(c)
			except IntegrityError:
				print "IntegrityError",str(IntegrityError)
				messages.error(request,"Integrity Error.",extra_tags="html_safe")
			except DatabaseError:
				print "DatabaseError",str(DatabaseError)
				messages.error(request,"Database Error.",extra_tags="html_safe")

	return render(request, 'Booking/my_rooms.html', {'list': list_nt})

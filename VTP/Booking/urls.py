from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
	url(r'^pilgrim/$', 'Booking.views.pilgrim_list', name='pilgrim_list'),
	url(r'^pilgrim/create/$', 'Booking.views.create_pilgrim', name='create_pilgrim'),
	url(r'^pilgrim/(?P<id>[0-9]{12})/edit/$', 'Booking.views.edit_pilgrim', name='edit_pilgrim'),
	url(r'^pilgrim/(?P<id>[0-9]{12})/delete/$', 'Booking.views.delete_pilgrim', name='delete_pilgrim'),
	url(r'^book/darshan/$', 'Booking.views.book_darshan', name='book_darshan'),
	url(r'^book/room/$', 'Booking.views.book_room', name='book_room'),	
	url(r'^book/room/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', 'Booking.views.book_room', name='book_room'),	
	url(r'^book/room/(?P<id>[0-9]{1,8})/$', 'Booking.views.book_room_darshan', name='book_room_darshan'),	
	url(r'^my_bookings/darshan/$', 'Booking.views.my_darshans', name='my_darshans'),	
	url(r'^my_bookings/room/$', 'Booking.views.my_rooms', name='my_rooms'),					
]

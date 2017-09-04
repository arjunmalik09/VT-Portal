from django.contrib.auth.models import User

from django import forms
from django.forms import extras
from datetime import date

genders = (('Male','Male'),('Female','Female'))
BIRTH_YEAR_CHOICES = [(date.today().year-i) for i in range(120)]

class PilgrimForm(forms.Form):
	aadhar_card_no = forms.CharField(max_length=12)
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	gender = forms.ChoiceField(choices=genders,widget=forms.RadioSelect)
	dob = forms.DateField(widget=forms.extras.SelectDateWidget(years=BIRTH_YEAR_CHOICES))

	def clean_aadhar_card_no(self): 
		aadhar_card_no = self.cleaned_data.get('aadhar_card_no')
		if not( len(aadhar_card_no) == 12 ):
		    raise forms.ValidationError("Enter valid aadhar_card_no! Aaadhar no length"+str(len(aadhar_card_no)))
		return aadhar_card_no

class PilgrimEditForm(forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	dob = forms.DateField(widget=forms.extras.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
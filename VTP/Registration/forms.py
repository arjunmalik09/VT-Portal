from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

import datetime

genders = (('Male','Male'),('Female','Female'))

class UserForm(forms.ModelForm) :
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta :
        model = User
        fields = ('first_name','last_name','email','password') 

class UserProfileForm(forms.ModelForm) :
    #username = forms.CharField(widget=forms.HiddenInput())
    gender = forms.ChoiceField(choices=genders,widget=forms.RadioSelect)

    class Meta :
        model = UserProfile
        fields = ('aadhar_card_no',
                'mobile_no',
                'gender',
                'apt_no',
                'locality_name',
                'city',
                'state',
                'pincode',
                'country')

    def clean_mobile_no(self): 
        mobile_no = self.cleaned_data.get('mobile_no')
        if not( len(mobile_no) == 10 ):
            raise forms.ValidationError("Enter valid mobile number!")
        return mobile_no

    def clean_aadhar_card_no(self): 
        aadhar_card_no = self.cleaned_data.get('aadhar_card_no')
        if not( len(aadhar_card_no) == 12 ):
            raise forms.ValidationError("Enter valid aadhar_card_no! Aaadhar no length"+str(len(aadhar_card_no)))
        return aadhar_card_no

class ProfileForm(forms.ModelForm) :
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta :
        model = UserProfile
        exclude = ('aadhar_card_no','gender','first_name','psswd')

    def clean_mobile_no(self): 
        mobile_no = self.cleaned_data.get('mobile_no')
        if not( len(mobile_no) == 10 ):
            raise forms.ValidationError("Enter valid mobile number!")
        return mobile_no
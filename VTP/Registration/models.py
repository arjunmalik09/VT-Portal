from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
#from .functions import n_day_hence
import datetime
# Create your models here.


class UserProfile(models.Model):
    aadhar_card_no = models.CharField(primary_key=True, max_length=12)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=60)
    mobile_no = models.CharField(unique=True, max_length=20)
    gender = models.CharField(max_length=10)
    apt_no = models.CharField(max_length=10)
    locality_name = models.CharField(max_length=80)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    username = models.CharField(unique=True, max_length=30)
    psswd = models.CharField(max_length=30)
    pincode = models.CharField(max_length=20)
    country = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'user_profile'


 
    # add fk
    # alter table user_profile add CONSTRAINT fk_user_prof_user FOREIGN KEY (username) references auth_user(username) on delete cascade on update cascade; 



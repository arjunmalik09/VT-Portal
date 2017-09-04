from django.db import models
from Registration.models import UserProfile
# Create your models here.
class Darshan(models.Model):
    price = models.IntegerField()
    max_bookings = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'darshan'

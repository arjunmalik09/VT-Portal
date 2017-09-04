from django.contrib import admin

# Register your models here.
from .models import UserProfile
#from .forms import 

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['username','email']
	#list_editable = ["job_profile",'status']
	#list_filter = ["visit_date","package"]
	#search_fields = ["remarks"]
	class Meta:
		model = UserProfile

admin.site.register(UserProfile,UserProfileAdmin)
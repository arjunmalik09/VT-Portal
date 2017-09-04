from django.contrib import admin

# Register your models here.
from .models import Darshan
#from .forms import 

class DarshanAdmin(admin.ModelAdmin):
	list_display = ['start_time','end_time']
	#list_editable = ["job_profile",'status']
	#list_filter = ["visit_date","package"]
	#search_fields = ["remarks"]
	class Meta:
		model = Darshan

admin.site.register(Darshan,DarshanAdmin)
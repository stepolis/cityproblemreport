from django.contrib import admin
from .models import *
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

class IncidencesAdmin(LeafletGeoAdmin):
	list_display = ('address', 'location', 'date', 'time', 'support_indicator',
					'problem_kind', 'user_username', 'user_email', 'status',
					'incident_slug')


class UsersAdmin(LeafletGeoAdmin):
	list_display = ('username', 'password', 'email', 'first_name', 'last_name',
					'car_driver', 'cellphone', 'visitor', 'visit_time', 'address',
					'is_staff', 'is_active', 'last_login', 'date_joined')


class ServManagerAdmin(LeafletGeoAdmin):
	list_display = ('service', 'username', 'password', 'email', 'service_slug')


class ProblemsAdmin(LeafletGeoAdmin):
	list_display = ('kind', 'hazard', 'picture', 'problem_slug')




admin.site.register(Incident, IncidencesAdmin)
admin.site.register(User_Res, UsersAdmin)
admin.site.register(Serv_Manager, ServManagerAdmin)
admin.site.register(Problems, ProblemsAdmin)

from django.conf.urls import include, url
from django.urls import path
from .import views
from djgeojson.views import GeoJSONLayerView
from .views import *
from .models import *



#Το url 'data/' είναι για τον χαρτη που έβαλα μετά στο index.htm

urlpatterns = [
	path('', views.homepage, name='home'),
	url(r'incidence_data/', point_datasets, name='incidences'),
	url(r'data/', GeoJSONLayerView.as_view(model=Incident, properties=('problem_kind', 'location'), geometry_field='location'), name='data'),
	path('register', views.register, name='register'),
	path('logout', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
    path("servicehome", views.servicehome, name="servicehome"),
    path('servicelogin', views.servicelogin_request, name='servicelogin'),
    path('account', views.account_request, name='account'),
    path("addform", views.add_or_change_incident, name="addform"),
    path("<single_slug>", views.single_slug, name="single_slug"),

]


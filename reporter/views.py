from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView
from django.core.serializers import serialize
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from .models import *
import json

# Create your views here.

class HomePageView(TemplateView):
	template_name = 'index.html'

def account_request(request):
	userid = str(request.user.id)
	return redirect(r'admin/auth/user/'+userid+'/change/')


@login_required(login_url='servicelogin')
def single_slug(request, single_slug):
	services_list = [s.service_slug for s in Serv_Manager.objects.all()]
	problems_list = [p.problem_slug for p in Problems.objects.all()]
	incidents_list = [str(j.incident_slug) for j in Incident.objects.all()]
	incident_list = [i.problem_kind for i in Incident.objects.all()]
	for s in Serv_Manager.objects.all():
		if s.service_slug == single_slug:
			service = s.service
	if single_slug in services_list:
		matching_problems = Problems.objects.filter(service__service_slug=single_slug)

		incidents_num = {}
		for m in matching_problems.all():
			incidents_num[m] = incident_list.count(m)

		return render(request=request,
				  template_name="services.html",
				  context={"service": service,
				  		  "services": Serv_Manager.objects.all,
				  		  "service_problems": matching_problems,
				  		  "incident_list": incident_list,
				  		  "incidents_num": incidents_num,
				  		  "user": request.user,})

	for p in Problems.objects.all():
		if p.problem_slug == single_slug:
			problem = p.kind
	if single_slug in problems_list:
		matching_incidents = Incident.objects.filter(problem_kind__problem_slug=single_slug)

		return render(request=request,
				  template_name="problems.html",
				  context={"problem": problem,
				  		  "services": Serv_Manager.objects.all,
				  		  "user_res": User_Res.objects.all,
				  		  "problem_incidents": matching_incidents,
				  		  "user": request.user,})

	if single_slug in incidents_list:
		for j in Serv_Manager.objects.all():
			if j.username == request.user.username:
				Incident.objects.filter(incident_slug=single_slug).update(status='SO')
		for j in User_Res.objects.all():
			if j.username == request.user.username:
				t = Incident.objects.get(incident_slug=single_slug)
				t.support_indicator = t.support_indicator+1
				t.save()
		for k in Incident.objects.all():
			if k.incident_slug == single_slug:
				for u in User_Res.objects.all():
					if u.username == k.user_username:
						user = u
						email_user(subject='Επίλυση Προβλήματος', message='Αγαπητέ χρήστη {user.username}, το πρόβλημα {match_incident} που καταχωρίσατε έχει λυθεί!!!', from_email=None)
		messages.success(request, f"Η επιλογή σας καταχωρήθηκε!!")
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

	return HttpResponse(f"{single_slug} δεν αντιστοιχεί σε κάτι!.")


def homepage(request):
	services_list = [s.service for s in Serv_Manager.objects.all()]
	incident_list = [i.problem_kind for i in Incident.objects.all()]
	problems_per_service = {}
	for se in services_list:
		matching_problems = Problems.objects.filter(service__service=se)
		problems_per_service[se] = matching_problems

	incidents_num = {}
	for m in Problems.objects.all():
		incidents_num[m] = incident_list.count(m)

	return render(request=request,
				  template_name="index.html",
				  context={"services": Serv_Manager.objects.all,
				  		  "problems": Problems.objects.all,
				  		  "incidents": Incident.objects.all,
				  		  "incidents_num": incidents_num,
				  		  "user": request.user,
				  		  "problems_per_service": problems_per_service})


def point_datasets(request):
	points = serialize('geojson', Incidences.objects.all())
	return HttpResponse(points, content_type='json')


def servicehome(request):
	services_list = [s.service for s in Serv_Manager.objects.all()]
	incident_list = [i.problem_kind for i in Incident.objects.all()]
	problems_per_service = {}
	for se in services_list:
		matching_problems = Problems.objects.filter(service__service=se)
		problems_per_service[se] = matching_problems

	messages.info(request, f"Επιλέψτε την υπηρεσία σας για να συνδεθείτε.")
	return render(request=request,
				  template_name="servicehome.html",
				  context={"services": Serv_Manager.objects.all,
				  		  "problems": Problems.objects.all,
				  		  "incidents": Incident.objects.all,
				  		  "problems_per_service": problems_per_service,
				  		  "user": request.user,})


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Ο νέος λογαριασμός δημιουργήθηκε: {username}.")
			login(request, user)
			messages.success(request, f"Έχετε συνδεθεί επιτυχώς ως {username}.")
			return redirect("home")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")


	form = NewUserForm
	return render(request,
				  "register.html",
				  context={"form":form,
				  		   "user": request.user,})


def logout_request(request):
	logout(request)
	messages.success(request, "Επιτυχής έξοδος!")
	return redirect("home")


def login_request(request):
	messages.info(request, f"Πριν καταχωρήσετε κάποιο Νέο Πρόβλημα, θα πρέπει να εισέλθετε με τους κωδικούς σας.")
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f"Έχετε συνδεθεί επιτυχώς ως {username}.")
				return redirect("home")
			else:
				messages.error(request, "Λανθασμένο username ή password!")
		else:
			messages.error(request, "Λανθασμένο username ή password!")

	form = AuthenticationForm()
	return render(request,
				  "login.html",
				  {"form":form,
				  "user": request.user,})
	

def servicelogin_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			for s in Serv_Manager.objects.all():
				if s.username == username:
					service_slug = s.service_slug
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Έχετε συνδεθεί επιτυχώς ως {username}")
				return redirect('single_slug', single_slug=service_slug)
			else:
				messages.error(request, "Λανθασμένο username ή password!")
		else:
			messages.error(request, "Λανθασμένο username ή password!")

	form = AuthenticationForm()
	return render(request,
				  "servicelogin.html",
				  {"form":form,
				  "user": request.user,})
	
@login_required(login_url='login')
def add_or_change_incident(request):
	messages.info(request, f"Στο πεδίο 'Τοποθεσία Προβλήματος' επιλέξτε το κουμπί με τον δείκτη (Draw a marker) και τοποθετήστε τον πάνω στον χάρτη.")
	if request.method == "POST":
		form = IncidentForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('user_username')
			incident = form.save()
			messages.success(request, f"Το Συμβάν-Πρόβλημα καταχωρήθηκε επιτυχώς από τον χρήστη: {username}.")
			return redirect("home")
			
		else:
			messages.error(request, "Το Συμβάν-Πρόβλημα δεν καταχωρήθηκε. Προσπαθήστε ξανά!")


	form = IncidentForm(request)
	form.fields["user_username"].queryset = User_Res.objects.filter(username=request.user)
	form.fields["user_email"].queryset = User_Res.objects.get(email=request.user.email)

	services_list = [s.service for s in Serv_Manager.objects.all()]
	incident_list = [i.problem_kind for i in Incident.objects.all()]
	problems_per_service = {}
	for se in services_list:
		matching_problems = Problems.objects.filter(service__service=se)
		problems_per_service[se] = matching_problems

	return render(request=request,
				  template_name="addform.html",
				  context={"services": Serv_Manager.objects.all,
				  		  "problems": Problems.objects.all,
				  		  "incidents": Incident.objects.all,
				  		  "problems_per_service": problems_per_service,
				  		  "user": request.user,
				  		  "form": form})


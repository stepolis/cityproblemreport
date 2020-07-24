from django.db import models
from django.contrib.auth.models import *
from django.contrib.gis.db import models
from datetime import *
from django.utils import timezone
import uuid

# Create your models here.


class User_Res(User):
	car_driver = models.BooleanField("Είστε Οδηγός Αυτοκινήτου?", null=True)
	cellphone = models.CharField("Κινητό Τηλέφωνο", max_length=10)
	visitor = models.BooleanField("Είστε Επισκέπτης στην Πόλη?", null=True)
	visit_time = models.DateField("Ημερομηνία Αναχώρησης", blank=True, null=True)
	address = models.PointField("Διεύθυνση Κατοικίας", srid=4326, blank=True, null=True)

	objects = UserManager()

	class Meta:
		verbose_name_plural = "Service Users"
		permissions = (("auth.change_user", "auth.view_user"),)

	def __unicode__(self):
		return self.username


class Serv_Manager(User):
	service = models.CharField("Υπηρεσία", max_length=50, primary_key=True)
	service_slug = models.SlugField()
	
	objects = UserManager()

	class Meta:
		verbose_name_plural = "Services"

	def __unicode__(self):
		return self.service


class Problems(models.Model):

	class Hazard(models.IntegerChoices):
		Mikri = 1, ('Μικρή')
		Mesaia = 2, ('Μεσαία')
		Megali = 3, ('Μεγάλη')
			
	kind = models.CharField("Είδος Προβλήματος", max_length=50, primary_key=True)
	service = models.ManyToManyField(Serv_Manager)
	hazard = models.IntegerField(choices=Hazard.choices)
	picture = models.ImageField("picture", blank=True, upload_to='media')
	problem_slug = models.SlugField(max_length=200)
	
	class Meta:
		verbose_name_plural = "Problems"
	
	def __str__(self):
		return self.kind
		

class Incident(models.Model):

	class Status(models.TextChoices):
		To_report = 'TR', ('Προς Εισαγωγή')
		Reported = 'RE', ('Εισηγμένο')
		To_solve = 'TS', ('Προς Επίλυση')
		Solved = 'SO', ('Λυμένο')
		Canceled = 'CA', ('Ακυρωμένο')

	address = models.CharField("Διεύθυνση", max_length=50, blank=True)
	location = models.PointField("Τοποθεσία Προβλήματος", srid=4326)
	date = models.DateField("Ημερομηνία Καταχώρησης", default=datetime.now())
	time = models.TimeField("Ώρα Καταχώρησης", default=datetime.now())
	support_indicator = models.IntegerField("Δείκτης Συμπαράστασης", default=1)
	problem_kind = models.ForeignKey(Problems, on_delete=models.CASCADE, verbose_name="Είδος Προβλήματος")
	user_username = models.ForeignKey(User_Res, on_delete=models.CASCADE, verbose_name="Όνομα Χρήστη")
	user_email = models.EmailField("Email Χρήστη", blank=True)
	status = models.CharField("Κατάσταση Προβλήματος", max_length=2, default='TR', choices=Status.choices)
	incident_slug = models.UUIDField(blank=True, default=uuid.uuid4, editable=False)

	class Meta:
		verbose_name_plural = "Incidents"

	def __unicode__(self):
		return self.location



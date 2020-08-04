from django import forms
from django.forms import ModelForm
from .models import *
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.contrib.gis.db import models
from django.contrib.gis import forms
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus import *



class NewUserForm(UserCreationForm):
	email = forms.EmailField(label=_("Email"), required=True, help_text=_("(Απαραίτητο! Εισάγετε το email σας σε έγκυρη μορφή.)"))
	address = forms.PointField(label='Διεύθυνση Κατοικίας', widget=LeafletWidget())
	password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, help_text=_("(Τουλάχιστον 8 χαρακτήρες!	Όχι ίδιο με προσωπικά στοιχεία!	Όχι μόνο αριθμούς!	Όχι συνηθισμένα passwords!)"))
	password2 = forms.CharField(label=_("Επαλήθευση Password"), widget=forms.PasswordInput, help_text=_("(Ξανά-εισάγετε το ίδιο password, όπως πριν, για επαλήθευση!)"))

	class Meta:
		model = User_Res
		fields = ("email", "username", "password1", "password2", "address", "first_name",
				  "last_name", "car_driver", "cellphone", "visitor", "visit_time")
		labels = {
			"first_name": _('Όνομα'), 
			"last_name": _('Επίθετο'), 
			"username": _('Username'),
			}
		help_texts = {
			"username": '(Απαραίτητο! Επιτρέπονται Ελληνικά, Λατινικά, Αριθμοί και τα Σύμβολα: @/./+/-/_ μόνο.)',
			}
		widgets = {
            "visit_time": DatePickerInput(format='%d/%m/%Y'),
            "address": LeafletWidget(),
        	}

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.is_staff=True
			user.save()
		return user


class IncidentForm(ModelForm):

	class Meta:
		model = Incident
		fields = ("location", "address", "problem_kind", "user_username", 
				  "user_email", "date", "time", "support_indicator", "status")
		help_texts = {
			"address": '(Προαιρετικό! Αν θέλετε συμπληρώστε και ονομαστικά την διεύθυνση του προβλήματος.)',
			"location": '(Απαραίτητο! Επιλέξτε πάνω στον χάρτη την ακριβή τοποθεσία του προβλήματος.)',
			"problem_kind": '(Απαραίτητο! Επιλέξτε από τη λίστα το είδος του προβλήματος.)',
			"user_username": '(Απαραίτητο! Συμπληρώστε το username σας.)',
			"user_email": '(Προαιρετικό! Συμπληρώστε εδώ το email σας, αν θέλετε να εμφανίζετε στις αναλυτικές πληροφορίες του προβλήματος, που θα βλέπουν οι υπόλοιποι χρήστες.)',
			}
		widgets = {
			"location": LeafletWidget(),
			}

	def __init__(self, request, *args, id_fields=None, ref_field=None, model=None, **kwargs):
		self.request = request
		self.id_fields = id_fields
		self.changed_fields = {}
		self.ref_field = ref_field
		self.model_ = model
		self.ref_id_changed = False

		super(IncidentForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		incident = super(IncidentForm, self).save(commit=False)
		if commit:
			incident.save()
		return incident


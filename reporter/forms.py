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
	email = forms.EmailField(required=True)
	address = forms.PointField(label='Διεύθυνση Κατοικίας', widget=LeafletWidget())
	password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, help_text=_("Τουλάχιστον 8 χαρακτήρες!	Όχι ίδιο με προσωπικά στοιχεία!	Όχι μόνο αριθμούς!	Όχι συνηθισμένα passwords!"))
	password2 = forms.CharField(label=_("Επαλήθευση Password"), widget=forms.PasswordInput, help_text=_("Εισάγετε το ίδιο password, όπως πριν, για επαλήθευση!"))

	class Meta:
		model = User_Res
		fields = ("email", "username", "password1", "password2", "address", "first_name",
				  "last_name", "car_driver", "cellphone", "visitor", "visit_time")
		labels = {
			"first_name": _('Όνομα'), 
			"last_name": _('Επίθετο'), 
			"password2": _('Επαλήθευση Password'),
			"username": _('Username (Όνομα Χρήστη)'),
			}
		help_texts = {
			"username": 'Απαραίτητο! Επιτρέπονται Ελληνικά, Λατινικά, Αριθμοί και τα Σύμβολα: @/./+/-/_ μόνο.',
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
		fields = ("location", "address", "date", "time", "support_indicator",
				  "problem_kind", "user_username", "user_email", "status")
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


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from quickstart.models import PatientProfile, DoctorProfile, Visit

class UserForm(UserCreationForm):
	first_name = forms.CharField(help_text='Required.')
	last_name = forms.CharField(help_text='Required.')
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name','email','password1', 'password2' )
		
class PatientProfileForm(forms.ModelForm):
	pesel = forms.DecimalField(help_text='Required. Format: DDDDDDDDDD')
	phone = forms.DecimalField(help_text='Required. Format: DDDDDDDDDD')
	isMale = forms.BooleanField(required=False,initial=False,label='Zaznacz, jeśli jesteś mężczyzną.')
	birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
	class Meta:
		model = PatientProfile
		fields = ('pesel', 'phone', 'birth', 'isMale')
		
class VisitFormP(forms.ModelForm):
	title = forms.CharField(help_text='Required. Format: DDDDDDDDDD. Maximum 100 characters')
	desc = forms.CharField(help_text='Required. Format: DDDDDDDDDD. Maximum 100 characters')
	doctor = forms.ModelChoiceField(queryset=DoctorProfile.objects.all(), help_text='Required.')
	date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
	class Meta:
		model = Visit
		fields = ('title', 'desc', 'doctor', 'date')
	def __init__(self, *args, **kwargs):
		super(VisitFormP, self).__init__(*args, **kwargs)
		self.fields['doctor'].label_from_instance = lambda obj: "%s" % obj.user.first_name + ' ' + obj.user.last_name
		
class VisitFormD(forms.ModelForm):
	title = forms.CharField(help_text='Required. Format: DDDDDDDDDD. Maximum 100 characters')
	desc = forms.CharField(help_text='Required. Format: DDDDDDDDDD. Maximum 300 characters')
	date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
	owner = forms.ModelChoiceField(queryset=PatientProfile.objects.all(), help_text='Required.', to_field_name="user")
	class Meta:
		model = Visit
		fields = ('title', 'desc', 'owner', 'date')
	def __init__(self, *args, **kwargs):
		super(VisitFormD, self).__init__(*args, **kwargs)
		self.fields['owner'].label_from_instance = lambda obj: "%s" % obj.user.first_name + ' ' + obj.user.last_name


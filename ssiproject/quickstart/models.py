from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from django.contrib.auth.models import User
from pygments import highlight
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PatientProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	birth = models.DateField(blank=True, default='2000-01-01')
	isMale = models.BooleanField(default = "False")
	pesel = models.DecimalField(max_digits=19, decimal_places=0, blank=True, default = "999",unique=True)
	phone = models.DecimalField(max_digits=11, decimal_places=0, blank=True, default = "999")
	
@receiver(post_save, sender=User)
def create_user_patientprofile(sender, instance, created, **kwargs):
    if created:
        PatientProfile.objects.create(user=instance)


class DoctorProfile(models.Model):
	user = models.ForeignKey(User, blank = False)
	phone = models.DecimalField(max_digits=11, decimal_places=0, blank = False)
	

class Visit(models.Model):
	date = models.DateTimeField(blank = False)
	title = models.CharField(max_length=100, blank = False)
	desc = models.TextField()
	isAccepted = models.BooleanField(default = False)
	owner = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, blank = False)
	doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, blank = False)
	class Meta:
		ordering = ('date',)




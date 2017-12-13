from django.contrib import admin
from quickstart.models import Visit, DoctorProfile, PatientProfile
# Register your models here.
admin.site.register(Visit)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
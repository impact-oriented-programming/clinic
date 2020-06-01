from django.contrib import admin
from .models import Doctor, Patient, Appointment

class Custoimize_Appointments(admin.ModelAdmin):
    list_display = ('id', 'date', 'start_time', 'doctor', 'patient', 'arrived_bool')
    list_filter = ['doctor', 'patient', 'room']

class Custoimize_Patient(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'clinic_identifying_number', 'visa_number')

class Custoimize_Doctor(admin.ModelAdmin):
    list_display = ('id', '__str__', 'specialty')


admin.site.register(Doctor, Custoimize_Doctor)
admin.site.register(Patient, Custoimize_Patient)
admin.site.register(Appointment, Custoimize_Appointments)

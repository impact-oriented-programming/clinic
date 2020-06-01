from django.contrib import admin
from .models import Doctor, Patient, Appointment


class Custoimize_Appointments(admin.ModelAdmin):
    list_display = ('id', 'date', 'start_time', 'doctor', 'patient')


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment, Custoimize_Appointments)


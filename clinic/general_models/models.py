import datetime
from django.db import models
from django.utils import timezone
import session

class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialty = models.CharField(max_length=30)
    email = models.EmailField()
    license_number = models.CharField(max_length=30)
    def __str__(self):
        return (self.first_name + " " + self.last_name)

class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    identifying_number = models.CharField(max_length=30)
    language = models.CharField(max_length=30, default='English')
    phone_number = models.CharField(max_length=30, blank=True)
    last_visit = models.DateField(blank=True)
    email = models.EmailField(blank=True)
    origin_country = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField()
    # sessions_list = 
    # family_members 
    def __str__(self):
        return (self.first_name + " " + self.last_name)

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return ("Appointment scheduled for: " + self.patient + "at: " + self.date + self.time + "with Doctor: " + self.doctor )
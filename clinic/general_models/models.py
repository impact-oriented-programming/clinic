import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from datetime import datetime, timedelta, date

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=30)
    license_number = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.user.first_name +' ' + self.user.last_name
    def __lt__(self, other):
        return str(self)<str(other)

@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created:
        Doctor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_doctor_profile(sender, instance, **kwargs):
    instance.doctor.save()

class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, null=True)
    clinic_identifying_number = models.CharField(max_length=30)
    visa_number = models.CharField(max_length=30)
    language = models.CharField(max_length=30, default='English')
    phone_number = models.CharField(max_length=30, blank=True)
    origin_country = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True)
    # family_members
    def __str__(self):
        return self.first_name + " " + self.last_name + "\n"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    time = models.TimeField()
    room = models.CharField(max_length=30, null=True)
    assigned = models.BooleanField( default=False) #is there a patient?
    arrived = models.BooleanField( default=False) # did the patient arrive to the reception desk at the scheduled day?
    done = models.BooleanField( default=False) # is the session done?
    

    @property
    def get_html_url(self):
        url = reverse('reception_desk:date-view', args=(str(self.date),)) # will sent the link to date view with argument - the appointment's date as string
        num_appointments = len(Appointment.objects.filter(date = self.date, assigned = True)) # we want th ecell in the calendar to say how many appointments are there for that day
        msg = 'scheduled appointment'
        if (num_appointments > 1): #plural in case of more than one appointment that day
            msg = msg + 's'
        if(date.today() == self.date):
            return f'<a style="text-decoration:none; color:white; font-size:16px" href="{url}">{num_appointments} {msg} </a>'
        return f'<a style="text-decoration:none; color:#366d6b; font-size:16px" href="{url}">{num_appointments} {msg} </a>'
    

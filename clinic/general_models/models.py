import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=30)
    license_number = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.user.username

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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    room = models.CharField(max_length=30, null=True)
    assigned = models.BooleanField( default=False)
    done = models.BooleanField( default=False)
    
    """
    @property
    def get_html_url(self):
        url = reverse('reception_desk:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    """
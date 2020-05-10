import datetime

from django.db import models
import general_models.models as gm
from django.urls import reverse

# view and manage all the appointments
# link to doctor_time_slot, 
# link to schedule
# calendar view of all the scheduled appointments
# mark a person that showed up to his appointemnt

# create a time slot in which a doctor is available to see patients
from django.utils import timezone


class DoctorSlot(models.Model):
    doctor = models.ForeignKey(gm.Doctor, on_delete=models.CASCADE)
    room = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    appointment_duration = models.IntegerField()


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
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=(datetime.time(7, 00)))
    end_time = models.TimeField(default=(datetime.time(21, 00)))
    appointment_duration = models.IntegerField()


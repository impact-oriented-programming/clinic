from django.db import models
import general_models.models as gm
import doctor_time_slot.models as slt
from django.urls import reverse

# view and manage all the appointments
# link to doctor_time_slot, 
# link to schedule
# calendar view of all the scheduled appointments
# mark a person that showed up to his appointemnt

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
import datetime
from django.db import models
from django.utils import timezone
import general_models.models as gm

class Session(models.Model):
     #doctor = models.ForeignKey(gm.Doctor, on_delete=models.CASCADE)
     patient = models.ForeignKey(gm.Patient, on_delete=models.CASCADE)
     time_of_session = models.DateTimeField('Time of Session')
     free_text = models.CharField(max_length=2000, blank=True)
     medications = models.CharField(max_length=2000, blank=True)
     special_request = models.CharField(max_length=2000, blank=True)
     
     def __init__(self, doctor, patient):
         self.doctor = doctor
         self.patient = patient
         self.time_of_session = timezone.now()

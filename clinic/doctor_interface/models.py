from django.db import models
from general_models.models import Patient, Doctor

class Session(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time = models.DateTimeField()
    chief_complaint = models.TextField(blank=True, null=True)
    physical_exam = models.TextField(blank=True, null=True)
    assessment = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)


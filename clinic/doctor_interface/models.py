from django.db import models
from general_models.models import Patient, Doctor


class Medication(models.Model):
    medication = models.CharField(max_length=100)
    medication_code = models.IntegerField()
    medication_details = models.TextField(blank=True, null=True)
    medication_yrpa_code = models.IntegerField(blank=True, null=True)
    medication_pharmasoft_code = models.IntegerField(blank=True, null=True)
    prescription_required = models.BooleanField()

    def __str__(self):
        return self.medication


class Diagnosis(models.Model):
    diagnosis = models.TextField()
    diagnosis_code = models.CharField(max_length=10)

    def __str__(self):
        return self.diagnosis


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
    height = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    systolic_bp = models.IntegerField(blank=True, null=True)
    diastolic_bp = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pulse = models.IntegerField(blank=True, null=True)
    respiratory_rate = models.IntegerField(blank=True, null=True)
    sp02 = models.IntegerField(blank=True, null=True)
    glucose = models.IntegerField(blank=True, null=True)

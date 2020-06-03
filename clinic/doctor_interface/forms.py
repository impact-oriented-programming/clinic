from django import forms
from .models import Session, BloodTestRequest, Diagnosis, Medication
from dal import autocomplete


class SessionForm(forms.ModelForm):

    diagnosis = forms.ModelChoiceField(
        queryset=Diagnosis.objects.all(),
        widget=autocomplete.ModelSelect2(url='doctor_interface:diagnosis-autocomplete')
    )
    prescriptions = forms.ModelChoiceField(
        queryset=Medication.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='doctor_interface:medication-autocomplete')
    )
    
    class Meta:
        model = Session
        fields = ['chief_complaint',
                  'physical_exam',
                  'assessment',
                  'treatment_plan',
                  'diagnosis',
                  'prescriptions',
                  'special_requests',
                  'height',
                  'weight',
                  'systolic_bp',
                  'diastolic_bp',
                  'temperature',
                  'pulse',
                  'respiratory_rate',
                  'sp02',
                  'glucose',
                  ]
        
class NewBloodTestForm(forms.ModelForm):

    class Meta:
        model = BloodTestRequest
        fields = ['blood_tests',
                  ]
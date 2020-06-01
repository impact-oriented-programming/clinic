from django import forms
from .models import Session, BloodTestRequest


class SessionForm(forms.ModelForm):

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
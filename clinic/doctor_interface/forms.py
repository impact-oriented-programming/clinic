from django import forms
from .models import Session


class SessionForm(forms.ModelForm):
    chief_complaint = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 5}))
    physical_exam = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 5}))
    assessment = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 5}))
    treatment_plan = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 5}))
    diagnosis = forms.CharField(required=False)
    prescriptions = forms.CharField(required=False)
    special_requests = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

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

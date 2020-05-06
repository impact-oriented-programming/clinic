from django import forms
from django.forms import ModelForm, fields, CheckboxInput
import general_models.models as gm
import pycountry
import datetime
from .models import DoctorSlot


class CreatePatientForm(ModelForm):
    origin_country = forms.ChoiceField(
        choices = sorted(((country.name, country.name) for country in pycountry.countries)),
        widget=forms.Select,
        required = True)

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years = list(range(datetime.datetime.now().year, 1900, -1))),
        required= True
    )

    gender = forms.ChoiceField(
        choices=(("f", "f"), ("m", "m")),
        widget=forms.Select,
        required=True
    )



    class Meta:
        model = gm.Patient
        fields = '__all__'


class DoctorSlotForm(forms.ModelForm):
    class Meta:
        model = DoctorSlot
        fields = '__all__'

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("Can'd add Doctor slot for passed Dates")
        return date

    def clean_end_time(self):
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        if end <= start:
            raise forms.ValidationError("End Time must be after Start Time")
        return end

    def clean_appointment_duration(self):
        appointment_duration = self.cleaned_data.get('appointment_duration')
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        if start is None or end is None:
            raise forms.ValidationError("")
        if doctor_slot_in_minutes(start, end) % appointment_duration != 0:
            raise forms.ValidationError("Doctor shift must divide in appointment duration")
        return appointment_duration


def doctor_slot_in_minutes(start, end):
    return (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)


class BoolForm(forms.ModelForm):
    # create meta class 
    class Meta: 
        # specify model to be used 
        model = gm.Appointment 
        # specify fields to be used 
        fields = ["arrived"]
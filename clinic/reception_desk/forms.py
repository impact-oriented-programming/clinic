import dal
from django import forms
from django.db.models import Q

from django.forms import ModelForm, fields, CheckboxInput

from django.forms import ModelForm

from django.contrib.admin import widgets
from django.forms import ModelForm

import general_models.models as gm
import pycountry
import datetime

from django.utils import timezone

from .models import DoctorSlot

HOUR_CHOICES = (
    [(datetime.time(hour=x, minute=y), '{:02d}:{:02d}'.format(x, y)) for x in range(8, 20) for y in range(00, 60, 10)])
APP_DURATION_CHOICES = (
    (10, '10'), (15, '15'), (20, '20'), (25, '25'), (30, '30'), (45, '45'))
ROOM_CHOICES = (
(None, ""), ("Blood Test AML", "Blood Test AML"), ("Refugee Clinic", "Refugee Clinic"), ("Nurse Room", "Nurse Room"),
("Ultrasound Room", "Ultrasound Room"), ("Room 1", "Room 1"), ("Room 2", "Room 2"), ("Room 3", "Room 3"),
("Room 4", "Room 4"), ("Room 5 Jerusalem", "Room 5 Jerusalem"), ("Room 6 Jerusalem", "Room 6 Jerusalem"),
("Room 7 Jerusalem", "Room 7 Jerusalem"))


class CreatePatientForm(ModelForm):
    origin_country = forms.ChoiceField(
        choices=sorted(((country.name, country.name) for country in pycountry.countries)),
        widget=forms.Select,
        required=True)

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=list(range(datetime.datetime.now().year, 1900, -1))),
        required=True
    )

    gender = forms.ChoiceField(
        choices=(("f", "Female"), ("m", "Male"), ("o", "Other")),
        widget=forms.Select,
        required=True
    )

    class Meta:
        model = gm.Patient
        fields = '__all__'


class DoctorSlotForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=gm.Doctor.objects.all())
    room = forms.CharField(widget=forms.Select(choices=ROOM_CHOICES), required=False)
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    start_time = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))
    end_time = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))
    appointment_duration = forms.IntegerField(widget=forms.Select(choices=APP_DURATION_CHOICES), initial=(10, '10'))

    class Meta:
        model = DoctorSlot
        fields = '__all__'

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("Can't add doctor time slot for passed dates")
        return date

    def clean_end_time(self):
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        if end <= start:
            raise forms.ValidationError("End time must be after start time")
        return end

    def clean_appointment_duration(self):
        appointment_duration = self.cleaned_data.get('appointment_duration')
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        if start is None or end is None:
            raise forms.ValidationError("")
        slot_gap = doctor_slot_in_minutes(start, end) % appointment_duration
        if slot_gap != 0:
            raise forms.ValidationError("Doctor shift must divide in appointment duration\n" +
                                        "(ending " + str(slot_gap) + " minutes earlier or " +
                                        str(appointment_duration - slot_gap) + " minutes later will work)")
        return appointment_duration

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        room = self.cleaned_data.get("room")
        if date and start and end:
            # Validate room only if all 3 fields are valid so far.
            if room is not None:
                appointments = gm.Appointment.objects.filter(date__range=(date, date)).filter(start_time__lt=end).filter(end_time__gt=start).filter(room__exact=room)
                if appointments.exists():
                    err = forms.ValidationError("This room is occupied for the requested time")
                    self.add_error('room', err)


def doctor_slot_in_minutes(start, end):
    return (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)


class BoolForm(forms.ModelForm):
    # create meta class 
    class Meta:
        # specify model to be used 
        model = gm.Appointment
        # specify fields to be used 
        fields = ["arrived"]


class EditPatientForm(ModelForm):
    origin_country = forms.ChoiceField(
        choices=sorted(((country.name, country.name) for country in pycountry.countries)),
        widget=forms.Select,
        required=True)

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=list(range(datetime.datetime.now().year, 1900, -1))),
        required=True
    )

    gender = forms.ChoiceField(
        choices=(("f", "f"), ("m", "m")),
        widget=forms.Select,
        required=True
    )

    class Meta:
        model = gm.Patient
        exclude = ['clinic_identifying_number']


class PatientInputForm(forms.Form):
    clinic_identifying_or_visa_number = forms.CharField(
        max_length=30,
        required=True
    )

    def clean_clinic_identifying_or_visa_number(self):
        id_number = self.cleaned_data.get('clinic_identifying_or_visa_number')
        patients = gm.Patient.objects.all()
        patients_filter = patients.filter(clinic_identifying_number=id_number)
        if len(patients_filter) == 0:
            patients_filter = patients.filter(visa_number=id_number)
        if len(patients_filter) == 0:
            raise forms.ValidationError("Patient Not Found")
            return id_number
        return id_number


class AppointmentEditForm(ModelForm):
    clinic_identifying_or_visa_number = forms.CharField(
        max_length=30,
        required=True,
    )

    class Meta:
        model = gm.Appointment
        fields = ['clinic_identifying_or_visa_number']

    def clean_clinic_identifying_or_visa_number(self):
        id_number = self.cleaned_data.get('clinic_identifying_or_visa_number')
        patients = gm.Patient.objects.all()
        patients_filter = patients.filter(clinic_identifying_number=id_number)
        if len(patients_filter) == 0:
            patients_filter = patients.filter(visa_number=id_number)
        if len(patients_filter) == 0:
            raise forms.ValidationError("Patient Not Found")
            return id_number
        return id_number

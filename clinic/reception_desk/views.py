from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
import datetime as dt
from .forms import CreatePatientForm, DoctorSlotForm, EditPatientForm, PatientInputForm
from django.contrib import messages
import general_models.models as gm
from .models import *
from .utils import Calendar
from collections import OrderedDict 


class CalendarView(generic.ListView):
    model = gm.Appointment
    template_name = 'reception_desk/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['today_date'] = str(date.today()) #to be used by today's appointments button
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def create_patient(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Account created for {first_name} {last_name}!')
            return redirect('reception_desk:calendar')
    else:
        form = CreatePatientForm()
    return render(request, 'reception_desk/create_new_patient.html', {'form': form, 'title': 'Create New Patient'})


def edit_patient(request, id_number):
    patients = gm.Patient.objects.all()
    patients_filter = patients.filter(clinic_identifying_number=id_number)
    if len(patients_filter) == 0:
        patients_filter = patients.filter(visa_number=id_number)
    patient = patients_filter.first()
    if request.method == 'POST':
        form = EditPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Information updated for {first_name} {last_name}!')
            return redirect('reception_desk:calendar')
    else:
        form = EditPatientForm(instance=patient)
    return render(request, 'reception_desk/edit_patient.html',  {'form': form, 'title': 'Edit Patient'})


def edit_existing_patient(request):
    if request.method == 'POST':
        form = PatientInputForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('clinic_identifying_or_visa_number')
            return redirect('reception_desk:edit-patient', id_number=id_number)
    else:
        form = PatientInputForm()
    return render(request, 'reception_desk/edit_existing_patient.html', {'form': form, 'title': 'Edit Patient Input'})


def doctor_slot_view(request):
    form = DoctorSlotForm(request.POST or None)
    if form.is_valid():
        slot_instance = form.save(commit=False)
        start = slot_instance.start_time
        delta = dt.timedelta(minutes=slot_instance.appointment_duration)
        # generate appointments
        while start < slot_instance.end_time:
            appointment = gm.Appointment.objects.create(doctor=slot_instance.doctor, patient=None, date=slot_instance.date,
                                                     time=start, room=slot_instance.room, assigned=False, done=False)
            appointment.save()
            start = add_delta_to_time(start, delta)
        form = DoctorSlotForm()  # redirect instead to calendar with message
    context = {'form': form, 'title': "Doctor time slot"}
    return render(request, 'reception_desk/doctor_time_slot.html', context)


def add_delta_to_time(time, delta):
    return (dt.datetime.combine(dt.date(1, 1, 1), time) + delta).time()


def date_view(request, my_date):
    # first parse wanted datr from given my_date string of form yyyy-mm-dd
    wanted_year = int(my_date[0:4])
    wanted_month = int(my_date[5:7])
    wanted_day = int(my_date[8:10])
    # make it a datetime.date instance
    try:
        wanted_date = date(wanted_year, wanted_month, wanted_day)
    except:
        return render(request,'reception_desk/date_error.html') #case the given date is not valid
    # list all the appointments of that given day
    appointment_list = gm.Appointment.objects.filter(date = wanted_date).order_by("time")
    # list all rooms
    rooms = sorted(set(appointment.room for appointment in  appointment_list))
    # list all doctors
    docs = sorted(set(appointment.doctor for appointment in  appointment_list))
    # crate a dictionary of room-->appointments list in that room
    drooms = OrderedDict()
    for room in rooms:
        drooms[room]=[]
    
    ddocs = OrderedDict()
    for doc in docs:
        ddocs[doc]=[]
        
    for appointment in appointment_list:
        drooms[appointment.room ].append(appointment)
        ddocs[appointment.doctor].append(appointment)

    context = {'drooms':drooms,'ddocs':ddocs,'wanted_date':wanted_date,'appointment_list':appointment_list}
    return render(request, 'reception_desk/date.html', context)
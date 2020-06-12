from datetime import datetime, timedelta, date

from django.db.models import Min, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
import datetime as dt
from .forms import CreatePatientForm, DoctorSlotForm, EditPatientForm, PatientInputForm, BoolForm, AppointmentEditForm, patient_from_id_number
from django.contrib import messages
import general_models.models as gm
from doctor_interface.models import Session
from .models import *
from .utils import Calendar
from collections import OrderedDict
from django.views import View
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist


# from django.contrib.auth.models import User


class CalendarView(generic.ListView):
    model = gm.Appointment

    def get_template_names(self, **kwargs):
        template_name = 'reception_desk/calendar.html'
        if not (self.request.user.is_authenticated):
            template_name = 'doctor_interface/not_logged_in.html'
        return [template_name]

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
        context['today_date'] = str(date.today())  # to be used by today's appointments button
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return dt.date(year, month, day=1)
    return dt.date.today()


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
    patient = patient_from_id_number(id_number)
    if patient is None:
        return redirect('reception_desk:calendar') #to be changed to patient does not exist page
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
    return render(request, 'reception_desk/edit_patient.html', {'form': form, 'title': 'Edit Patient'})


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
            appointment = gm.Appointment.objects.create(doctor=slot_instance.doctor, patient=None,
                                                        date=slot_instance.date, start_time=start,
                                                        end_time=add_delta_to_time(start, delta),
                                                        room=slot_instance.room, assigned=False, done=False)
            appointment.save()
            start = add_delta_to_time(start, delta)
        messages.success(request, f'Doctor time slot added successfully!')
        return redirect('reception_desk:calendar')
    context = {'form': form, 'title': "Doctor time slot"}
    return render(request, 'reception_desk/doctor_time_slot.html', context)


def add_delta_to_time(time, delta):
    return (dt.datetime.combine(dt.date(1, 1, 1), time) + delta).time()


def date_view(request, my_date):

    if request.method == 'POST':
        appointment_id = request.POST.get('arrived')
        appointment = gm.Appointment.objects.all().get(id=appointment_id)
        appointment.arrived = dt.datetime.now().time()
        appointment.save()
        return redirect('reception_desk:date-view', my_date=my_date)

    # first parse wanted date from given my_date string of form yyyy-mm-dd
    wanted_year = int(my_date[0:4])
    wanted_month = int(my_date[5:7])
    wanted_day = int(my_date[8:10])
    # make it a datetime.date instance
    try:
        wanted_date = date(wanted_year, wanted_month, wanted_day)
    except:
        return render(request, 'reception_desk/date_error.html')  # case the given date is not valid
    # list all the appointments of that given day
    appointment_list = gm.Appointment.objects.filter(date=wanted_date).order_by("start_time")
    appointment_list = appointment_list.filter(assigned=True)
    # list all rooms
    rooms = sorted(set(appointment.room for appointment in appointment_list))
    # list all doctors
    docs = sorted(set(appointment.doctor for appointment in appointment_list))
    # crate a dictionary of room-->appointments list in that room
    drooms = OrderedDict()
    for room in rooms:
        drooms[room] = []

    ddocs = OrderedDict()
    for doc in docs:
        ddocs[doc] = []

    for appointment in appointment_list:
        drooms[appointment.room].append(appointment)
        ddocs[appointment.doctor].append(appointment)

    context = {'drooms': drooms, 'ddocs': ddocs, 'wanted_date': wanted_date,
               'appointment_list': appointment_list}

    return render(request, 'reception_desk/date.html', context)


class clinic_management(View):
    def get(self, request, *args, **kwargs):
        # if not (request.user.is_authenticated):
        #   return render(request, 'doctor_interface/not_logged_in.html')
        # context = {}
        return render(request, 'reception_desk/clinic_management.html')


def add_appointment_view(request):
    context = get_params(request, 'Add Appointment')
    appointments = gm.Appointment.objects.all().filter(assigned=False).order_by('date', 'start_time')
    appointments = filter_appointments(context, appointments)
    paginate(context, appointments)
    return render(request, 'reception_desk/add_appointment.html', context)


def cancel_appointment_view(request):
    if request.method == "POST":
        remove_id = request.POST.get('remove_id')
        if is_valid_param(remove_id):
            clear_appointment(appointments, remove_id)
    context = get_params(request, 'Cancel Appointment')
    appointments = gm.Appointment.objects.all().filter(assigned=True).order_by('date', 'start_time')
    appointments = filter_appointments(context, appointments)
    if is_valid_param(context.get('patient')):
        appointments = [appointment for appointment in appointments if
                        appointment.patient.visa_number == context.get('patient') or
                        appointment.patient.clinic_identifying_number == context.get('patient')]
    context['appointments'] = appointments
    paginate(context, appointments)
    return render(request, 'reception_desk/cancel_appointment.html', context)


class AppointmentAssignView(generic.UpdateView):
    model = gm.Appointment
    form_class = AppointmentEditForm
    template_name = 'reception_desk/appointment_assign.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Make Appointment'
        return context

    def get_success_url(self):
        return reverse('reception_desk:add-appointment')

    def form_valid(self, form):
        id_number = form.cleaned_data.get('clinic_identifying_or_visa_number')
        patient = patient_from_id_number(id_number)
        if patient is not None:
            form.instance.patient = patient
            form.instance.assigned = True
            messages.success(self.request, f'Appointment set for {patient.first_name} {patient.last_name}!')
        return super().form_valid(form)


def walk_in_view(request):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    today_appointments = gm.Appointment.objects.filter(date__exact=date.today())
    today_shifts = today_appointments.values('doctor', 'room').annotate(start=Min('start_time'), end=Max('end_time'))
    curr_time = dt.datetime.now().time()
    today_relevant_shifts = [shift for shift in today_shifts if shift['start'] < curr_time < shift['end']]
    doctors_dict = {gm.Doctor.objects.get(id=today_relevant_shifts[i]['doctor']): [today_relevant_shifts[i]['room'], today_relevant_shifts[i]['end']] for i in range(len(today_relevant_shifts))}
    context = {"doctors_dict": doctors_dict, 'title': "Walk-In"}
    return render(request, 'reception_desk/walk_in.html', context)


def walk_in_schedule_view(request, doctor_id, room):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    doctor = gm.Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = PatientInputForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('clinic_identifying_or_visa_number')
            patient = patient_from_id_number(id_number)
            curr_time = dt.datetime.now().time()
            curr_date = dt.datetime.now().today()
            appointment = gm.Appointment.objects.create(doctor=doctor, patient=patient, date=curr_date,
                                                        start_time=curr_time, end_time=curr_date+timedelta(minutes=10),
                                                        room=room, assigned=True, arrived=curr_time, done=False)
            appointment.save()
            messages.success(request, f'Walk-In added for {patient}!')
            return redirect('reception_desk:calendar')
    else:
        form = PatientInputForm()
    context = {"doctor": doctor, 'room': room, "form": form, 'title': "Schedule Walk-In"}
    return render(request, 'reception_desk/walk_in_schedule.html', context)


### aid functions ###

def is_valid_param(param):
    return param != '' and param is not None


def get_specialities(doctors):
    specialties = set(['All'])
    for doctor in doctors:
        if is_valid_param(doctor.specialty):
            specialties.add(doctor.specialty)
    return sorted(list(specialties))


def get_params(request, title):
    context = {'title': title, 'doctors': gm.Doctor.objects.all(),
               'specialty': request.GET.get('specialty'), 'from_date': request.GET.get('from_date'),
               'until_date': request.GET.get('until_date'), 'doctor': request.GET.get('doctor'),
               'page_number': request.GET.get('page')}
    context['specialties'] = get_specialities(context.get('doctors'))
    context['doctors'] = ['All'] + sorted([str(doctor) for doctor in context['doctors']])
    if context.get('from_date') is None:
        context['from_date'] = date.today().strftime('%Y-%m-%d')
    return context


def filter_appointments(context, appointments):
    if is_valid_param(context.get('from_date')):
        appointments = appointments.filter(date__gte=context.get('from_date'))
    if is_valid_param(context.get('until_date')):
        appointments = appointments.filter(date__lte=context.get('until_date'))
    if is_valid_param(context.get('specialty')) and context.get('specialty') != "All":
        appointments = [appointment for appointment in appointments if
                        appointment.doctor.specialty == context.get('specialty')]
    if is_valid_param(context.get('doctor')) and context.get('doctor') != 'All':
        appointments = [appointment for appointment in appointments if
                        str(appointment.doctor) == context.get('doctor')]
    return appointments


def paginate(context, appointments):
    appointments_per_page = 9
    paginator = Paginator(appointments, appointments_per_page)
    if is_valid_param(context.get('page_number')):
        page_obj = paginator.get_page(context.get('page_number'))
    else:
        page_obj = paginator.get_page(1)
    context['page_obj'] = page_obj
    if len(appointments) > appointments_per_page:
        context['is_paginated'] = True
    elif len(appointments) == 0:
        context['empty'] = True
    return context


def clear_appointment(appointments, remove_id):
    appointment_to_clear = appointments.get(id=remove_id)
    if appointment_to_clear.assigned:
        appointment_to_clear.patient = None
        appointment_to_clear.assigned = False
        appointment_to_clear.save()


### end of aid functions ###


def view_patient(request):
    if not (request.user.is_authenticated):
        return render(request, 'doctor_interface/not_logged_in.html')

    user = request.user
    if request.method == 'POST':
        form = PatientInputForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('clinic_identifying_or_visa_number')
            return redirect('reception_desk:patient-details', id_number=id_number)
    else:
        form = PatientInputForm()
    context = {"user": user, 'form':form, 'title': 'View Patient'}
    return render(request, 'reception_desk/view_patient_form.html', context)


def patient_details(request, id_number):
    if not (request.user.is_authenticated):
        return render(request, 'doctor_interface/not_logged_in.html')

    patient_filter = patient_from_id_number(id_number)
    if patient_filter is None:
        return render(request, 'doctor_interface/error_patient_not_found.html')  # TODO - fix return button to calendar

    last_visits = Session.objects.all()
    max_session = min(5, len(last_visits))
    last_visits = last_visits.filter(patient=patient_filter)[:max_session]
    context = {'patient': patient_filter, 'last_visits': last_visits}  # , "age": str(age)}
    return render(request, 'reception_desk/view_patient.html', context)




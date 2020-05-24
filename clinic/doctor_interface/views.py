from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
import general_models.models as gm
import datetime
from .forms import SessionForm
from .models import Session
from django.utils import timezone
import django.contrib.auth
from django.contrib import messages
from reception_desk.forms import PatientInputForm


def index_patient(request, clinic_id):
    if not (request.user.is_authenticated):
        return render(request, 'doctor_interface/not_logged_in.html')
    if not (request.user.groups.filter(name='Doctors').exists()):
        return render(request, 'doctor_interface/not_a_doctor.html')
    patient = gm.Patient.objects.all()
    patient_filter = patient.filter(clinic_identifying_number=clinic_id)
    if (len(patient_filter)==0):
        patient_filter = patient.filter(visa_number=clinic_id)
    if (len(patient_filter)==0): # patient not found - will only happen if trying directly through url
        return render(request, 'doctor_interface/error_patient_not_found.html')
       
    patient_filter = patient_filter[0]  # was list of length 1. we want the patient itselfs
    #age = datetime.datetime.now().year
    last_visits = Session.objects.all()
    max_session = min(5, len(last_visits))
    last_visits = last_visits.filter(patient=patient_filter)[:max_session]
    context = {'patient': patient_filter, 'last_visits': last_visits} #, "age": str(age)}
    return render(request, 'doctor_interface/patient_interface_home.html', context)


def index(request):
    if not (request.user.is_authenticated):
        return render(request, 'doctor_interface/not_logged_in.html')
    if not (request.user.groups.filter(name='Doctors').exists()):
        return render(request, 'doctor_interface/not_a_doctor.html')

    user = request.user
    # specialty = user.doctor.specialty
    my_appointments = gm.Appointment.objects.all()
    my_appointments = my_appointments.filter(assigned=True)
    my_appointments = my_appointments.filter(doctor=user.doctor)
    my_appointments = my_appointments.filter(done=False)
    today_appointments = my_appointments.filter(date=str(datetime.date.today())).order_by("start_time")
    
    # for browse patient:
    if request.method == 'POST':
        form = PatientInputForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('clinic_identifying_or_visa_number')
            return redirect('doctor_interface:patient_interface', clinic_id = id_number)
    else:
        form = PatientInputForm()
    
    context = {"user": user, "today_appointments": today_appointments, 'form':form}

    return render(request, 'doctor_interface/doctor_interface_home.html', context)


def new_session_view(request, clinic_id):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    if not (request.user.groups.filter(name='Doctors').exists()):
        return render(request, 'doctor_interface/not_a_doctor.html')
    form = SessionForm(request.POST or None)
    patient = gm.Patient.objects.all().filter(clinic_identifying_number=clinic_id)[0]
    if form.is_valid():
        session = form.save(commit=False)
        session.doctor = request.user.doctor
        session.patient = patient
        session.time = timezone.now()
        session.save()
        messages.success(request, f'Session saved!')
        return redirect('doctor_interface:patient_interface', clinic_id=clinic_id)

    context = {'form': form, 'title': "New Session", 'patient': patient}
    return render(request, 'doctor_interface/session.html', context)


def session_edit_view(request, clinic_id, pk):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    if not (request.user.groups.filter(name='Doctors').exists()):
        return render(request, 'doctor_interface/not_a_doctor.html')
    session = get_object_or_404(Session, pk=pk)
    patient = gm.Patient.objects.all().filter(clinic_identifying_number=clinic_id)[0]
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.doctor = request.user.doctor
            session.patient = patient
            session.time = timezone.now()
            session.save()
            messages.success(request, f'Session edited successfully!')
            return redirect('doctor_interface:patient_interface', clinic_id=clinic_id)
    else:
        form = SessionForm(instance=session)

    context = {'form': form, 'title': "Edit Session", 'patient': patient}
    return render(request, 'doctor_interface/session.html', context)

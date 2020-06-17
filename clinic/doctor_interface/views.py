from dal import autocomplete
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import View as generic_view
import general_models.models as gm
from clinic.utils import render_to_pdf
import datetime
from .forms import SessionForm, NewBloodTestForm
import datetime as dt
from .forms import SessionForm
from .models import Session, Diagnosis, Medication, BloodTest, BloodTestRequest
from django.utils import timezone
import django.contrib.auth
from django.contrib import messages
from reception_desk.forms import PatientInputForm, patient_from_id_number
from django.core.exceptions import ObjectDoesNotExist


def index_patient(request, clinic_id):
    if not (request.user.is_authenticated):
        return render(request, 'doctor_interface/not_logged_in.html')
    try:
        request.user.doctor
    except:
        return render(request, 'doctor_interface/not_a_doctor.html')
    patient = patient_from_id_number(clinic_id)
    if patient is None:
        return render(request, 'doctor_interface/error_patient_not_found.html')

    patient_age = calculate_patient_age(patient)
    last_visits = Session.objects.all().filter(patient=patient).order_by('-time')
    max_session = min(5, len(last_visits))
    last_visits = last_visits[:max_session]
    last_meds = []
    for session in last_visits:
        for med in session.prescriptions.all():
            last_meds.append((med, session.time, session.doctor))
    max_meds = min(5, len(last_meds))
    last_meds = last_meds[:max_meds]
    last_blood = BloodTestRequest.objects.all().filter(patient=patient).order_by('-time')
    max_blood = min(5, len(last_blood))
    last_blood = last_blood[:max_blood]
    context = {
            'patient': patient,
            'last_visits': last_visits,
            'age_value': str(patient_age),
            'last_meds': last_meds,
            'last_blood': last_blood
               }
    return render(request, 'doctor_interface/patient_interface_home.html', context)


def index(request):
    if not (request.user.is_authenticated):
        return render(request, 'doctor_interface/not_logged_in.html')
    try:
        request.user.doctor
    except:
        return render(request, 'doctor_interface/not_a_doctor.html')

    user = request.user
    # specialty = user.doctor.specialty
    my_appointments = gm.Appointment.objects.all()
    my_appointments = my_appointments.filter(assigned=True)
    my_appointments = my_appointments.filter(doctor=user.doctor)
    my_appointments = my_appointments.filter(done=False)
    today_appointments = my_appointments.filter(date=str(datetime.date.today())).order_by("start_time")
    app_arrived = []
    app_not_arrived = []
    for app in today_appointments:
        if not app.arrived:
            app_not_arrived.append(app)
        else:
            app_arrived.append(app)
    curr_time = dt.datetime.now().time()
    # for browse patient:
    if request.method == 'POST':
        form = PatientInputForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('clinic_identifying_or_visa_number')
            return redirect('doctor_interface:patient_interface', clinic_id = id_number)
    else:
        form = PatientInputForm()
    
    context = {"user": user, "today_appointments": today_appointments, "curr_time": curr_time, "app_arrived":app_arrived, "app_not_arrived":app_not_arrived,  'form':form}

    return render(request, 'doctor_interface/doctor_interface_home.html', context)


def new_session_view(request, clinic_id):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    try:
        request.user.doctor
    except:
        return render(request, 'doctor_interface/not_a_doctor.html')
    form = SessionForm(request.POST or None)
    patient = gm.Patient.objects.get(clinic_identifying_number=clinic_id)
    if form.is_valid():
        session = form.save(commit=False)
        session.doctor = request.user.doctor
        session.patient = patient
        session.time = timezone.now()
        form.save()
        session.save()
        messages.success(request, f'Session saved!')
        return redirect('doctor_interface:patient_interface', clinic_id=clinic_id)

    context = {'form': form, 'title': "New Session", 'patient': patient}
    return render(request, 'doctor_interface/session.html', context)


def session_edit_view(request, clinic_id, pk):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    try:
        request.user.doctor
    except:
        return render(request, 'doctor_interface/not_a_doctor.html')
    session = get_object_or_404(Session, pk=pk)
    patient = gm.Patient.objects.all().filter(clinic_identifying_number=clinic_id)[0]
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
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


def new_blood_test_view(request, clinic_id):
    if not request.user.is_authenticated:
        return render(request, 'doctor_interface/not_logged_in.html')
    try:
        request.user.doctor
    except:
        return render(request, 'doctor_interface/not_a_doctor.html')
    form = NewBloodTestForm(request.POST or None)
    doctor = request.user.doctor
    patient = gm.Patient.objects.get(clinic_identifying_number=clinic_id)
    patient_age = calculate_patient_age(patient)
    current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if form.is_valid():
        blood_test_request = form.save(commit=False)
        blood_test_request.doctor = doctor
        blood_test_request.patient = patient
        blood_test_request.time = timezone.now()
        form.save()
        blood_test_request.save()
        messages.success(request, f'Blood test saved!')
        return redirect('doctor_interface:patient_interface', clinic_id=clinic_id)

    context = {'form': form, 'patient': patient, 'doctor': doctor, 'age_value': str(patient_age), 'current_time': str(current_time)}
    return render(request, 'doctor_interface/blood_test_request.html', context)

class DiagnosisAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Diagnosis.objects.all()

        if self.q:
            qs = qs.filter(description__icontains=self.q)

        return qs
    
class MedicationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Medication.objects.all()

        if self.q:
            qs = qs.filter(medication__istartswith=self.q)

        return qs
    
class BloodTestAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = BloodTest.objects.all()

        if self.q:
            qs = qs.filter(blood_test__istartswith=self.q)

        return qs
    
    
def GenerateMedsPDF(request, pk):
        session = get_object_or_404(Session, pk=pk)
        age = calculate_patient_age(session.patient)
        prescription_meds = session.prescriptions.all().filter(prescription_required=True)
        none_prescription_meds = session.prescriptions.all().filter(prescription_required=False)
        context = {
             'session': session, 
             'date': datetime.date.today(),
             'age_value': str(age),
             'prescription_meds': prescription_meds,
             'none_prescription_meds': none_prescription_meds
        }
        pdf = render_to_pdf('doctor_interface/pdf/export_medication.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    
def GenerateBloodTestPDF(request, pk):
        blood_test_request = get_object_or_404(BloodTestRequest, pk=pk)
        age = calculate_patient_age(blood_test_request.patient)
        context = {
             'blood_test_request': blood_test_request, 
             'date': datetime.date.today(),
             'age_value': str(age),
        }
        pdf = render_to_pdf('doctor_interface/pdf/export_blood_test.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    
    
####Helper Functions####
    
def calculate_patient_age(patient):
    
    today = datetime.date.today()
    born = patient.date_of_birth
    patient_age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return patient_age
    
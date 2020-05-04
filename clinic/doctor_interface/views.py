from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import general_models.models as gm
import datetime
from django.utils import timezone
import django.contrib.auth

class index_patient(View):
    
    def get(self, request, *args, **kwargs):
        
        all_patients = gm.Patient.objects.all()
        testing_patient = all_patients[0]
        all_patient_appointments = gm.Appointment.objects.all()
        all_patient_appointments = all_patient_appointments.filter(patient = testing_patient).order_by("date")
        
        context = {
            'patient': testing_patient, 
            'last_visits': all_patient_appointments
            }
        return render(request, 'doctor_interface/patient_interface_home.html', context)
        



class index(View):

    def get(self, request, *args, **kwargs):
        if not(request.user.is_authenticated):
            return render(request, 'doctor_interface/not_logged_in.html')
        if not(request.user.groups.filter(name = 'Doctors').exists()):
            return render(request, 'doctor_interface/not_a_doctor.html')
        
        user = request.user
        specialty = user.doctor.specialty
        my_appointments = gm.Appointment.objects.all()
        my_appointments = my_appointments.filter(assigned = True)
        my_appointments = my_appointments.filter(doctor = user.doctor)
        my_appointments = my_appointments.filter(done = False)
        today_appointments = my_appointments.filter(date = str(datetime.date.today())).order_by("time")
        
        context = {"user": user,  "today_appointments": today_appointments }

        return render(request, 'doctor_interface/doctor_interface_home.html', context)
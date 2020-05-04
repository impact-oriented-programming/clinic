from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import general_models.models as gm

#def index(request):
#    return HttpResponse("Hello, world. You're at the CLINIC CALENDAR index.")

class index(View):
    
    def get(self, request, *args, **kwargs):
        
        all_patients = gm.Patient.objects.all()
        testing_patient = all_patients[0]
        all_patient_appointments = gm.Appointment.objects.all()
        all_patient_appointments = all_patient_appointments.filter(patient = testing_patient).order_by("date")
        
        context = {
            'patient': testing_patient, 
            'last_visits': all_patient_appointments
            }
        return render(request, 'patient_interface/patient_interface_home.html', context)
        


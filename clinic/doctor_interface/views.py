from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import general_models.models as gm
import datetime
from django.utils import timezone

def index2(request):
    return HttpResponse("Hello, world. You're at the CLINIC CALENDAR index.")


class index(View):

    def get(self, request, *args, **kwargs):

        user = request.user
        specialty = user.doctor.specialty
        all_appointments = gm.Appointment.objects.all()
        my_appointments = all_appointments.filter(doctor = user.doctor)
        today_appointments = my_appointments.filter(date = str(datetime.date.today()))
        
        context = {"user": user,  "today_appointments": today_appointments }

        return render(request, 'doctor_interface/doctor_interface_home.html', context)
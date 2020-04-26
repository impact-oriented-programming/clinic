from django.shortcuts import render
from django.http import HttpResponse


#def login(request):
#    return render(request, 'doctor_interface/login.html')


def index(request):
    return HttpResponse("Hello, world. You're at the DOCTOR INTERFACE index.")

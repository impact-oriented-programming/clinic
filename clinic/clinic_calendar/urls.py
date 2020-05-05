from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'clinic_calendar'
urlpatterns = [
    path('calendar', views.CalendarView.as_view(), name='calendar'),
    path('create-patient', views.create_patient, name='create-patient'),
    path('doctor-time-slot', views.doctor_slot_view, name='doctor-time-slot'),
]
from django.urls import path
from django.conf.urls import url
from datetime import datetime, timedelta, date
from . import views

app_name = 'reception_desk'
urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('create-patient/', views.create_patient, name='create-patient'),
    path('doctor-time-slot/', views.doctor_slot_view, name='doctor-time-slot'),
    path('date-view/<str:my_date>', views.date_view, name='date-view'),
    path('edit-patient/<id_number>', views.edit_patient, name='edit-patient'),
    path('edit-existing-patient/', views.edit_existing_patient, name='edit-existing-patient'),
    path('clinic-management', views.clinic_management.as_view() , name='clinic-management'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment'),
    path('appointment/<int:pk>/assign/', views.AppointmentAssignView.as_view(), name='appointment-assign'),
    path('appointments/', views.appointments_view, name='appointments'),
]

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
    path('clinic-management', views.clinic_management.as_view(), name='clinic-management'),
    path('appointment/<int:pk>/assign/', views.AppointmentAssignView.as_view(), name='appointment-assign'),
    path('add-appointment/', views.add_appointment_view, name='add-appointment'),
    path('view-patient/', views.view_patient, name='view-patient'),
    path('patient-details/<id_number>', views.patient_details, name='patient-details'),
    path('walk-in/', views.walk_in_view, name='walk-in'),
    path('walk-in-schedule/<doctor_id>/<str:room>', views.walk_in_schedule_view, name='walk-in-schedule'),
    path('cancel-appointment/', views.cancel_appointment_view, name='cancel-appointment'),
    path('appointments', views.Appointments.as_view(), name='appointments'),
]

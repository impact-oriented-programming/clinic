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
    url(r'^doctor-autocomplete/$', views.doctor_autocomplete.as_view(), name='doctor-autocomplete')
]
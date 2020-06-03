from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

app_name = 'doctor_interface'
urlpatterns = [
    path('', views.index , name='homepage'),
    path('patient_interface/<clinic_id>', views.index_patient, name='patient_interface'),
    path('patient_interface/<str:clinic_id>/new-session', views.new_session_view, name='new-session'),
    path('patient_interface/<str:clinic_id>/<int:pk>/edit-session', views.session_edit_view, name='edit-session'),
    path('patient_interface/<str:clinic_id>/blood-test', views.new_blood_test_view, name='blood-test'),
    url(r'^diagnosis-autocomplete/$', views.DiagnosisAutocomplete.as_view(), name='diagnosis-autocomplete'),
    url(r'^medication-autocomplete/$', views.MedicationAutocomplete.as_view(), name='medication-autocomplete'),
    path('patient_interface/<int:pk>/medication-pdf', views.GeneratePDF, name='medication-pdf')
    ]
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

app_name = 'doctor_interface'
urlpatterns = [
    path('', views.index.as_view() , name='homepage'),
    path('patient_interface/<str:clinic_id>', views.index_patient , name='patient_interface'),
    ]

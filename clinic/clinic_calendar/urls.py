from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'clinic_calendar'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
]
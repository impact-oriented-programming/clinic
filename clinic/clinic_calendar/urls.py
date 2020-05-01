from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'clinic_calendar'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    url('event/new/', views.event, name='event_new'),
    url('event/edit/(?P<event_id>\d+)/', views.event, name='event_edit')
]
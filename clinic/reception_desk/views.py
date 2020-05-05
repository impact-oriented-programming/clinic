from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
import datetime as dt
from .forms import CreatePatientForm, DoctorSlotForm
from django.contrib import messages
import general_models.models as gm
from .models import *
from .utils import Calendar

class CalendarView(generic.ListView):
    model = gm.Appointment
    template_name = 'reception_desk/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def create_patient(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Account created for {first_name} {last_name}!')
            return redirect('reception_desk:calendar')
    else:
        form = CreatePatientForm()
    return render(request, 'reception_desk/create_new_patient.html', {'form': form, 'title': 'Create New Patient'})


def doctor_slot_view(request):
    form = DoctorSlotForm(request.POST or None)
    if form.is_valid():
        slot_instance = form.save(commit=False)
        start = slot_instance.start_time
        delta = dt.timedelta(minutes=slot_instance.appointment_duration)
        # generate appointments
        while start < slot_instance.end_time:
            appointment = gm.Appointment.objects.create(doctor=slot_instance.doctor, patient=None, date=slot_instance.date,
                                                     time=start, room=slot_instance.room, assigned=False, done=False)
            appointment.save()
            start = add_delta_to_time(start, delta)
        form = DoctorSlotForm()  # redirect instead to calendar with message
    context = {'form': form, 'title': "Doctor time slot"}
    return render(request, 'reception_desk/doctor_time_slot.html', context)


def add_delta_to_time(time, delta):
    return (dt.datetime.combine(dt.date(1, 1, 1), time) + delta).time()


def date_view(request, my_date):
    today_date = date.today()
    context = {'date':my_date, 'today_date':today_date}
    return render(request, 'reception_desk/date.html', context)
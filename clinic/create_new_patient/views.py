from django.shortcuts import render, redirect
from .forms import CreatePatientForm
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Account created for {first_name} {last_name}!')
            return redirect('clinic_calendar:calendar')
    else:
        form = CreatePatientForm()
    return render(request, 'create_new_patient/create_new_patient.html', {'form': form, 'title': 'Create New Patient'})




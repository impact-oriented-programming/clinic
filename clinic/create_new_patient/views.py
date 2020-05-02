from django.shortcuts import render, redirect
from .forms import CreatePatientForm


def index(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePatientForm()
    return render(request, 'create_new_patient/create_new_patient.html', {'form': form})




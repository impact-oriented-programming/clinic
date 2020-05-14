from django.contrib import admin
from .models import Medication, Diagnosis, Session

admin.site.register(Medication)
admin.site.register(Diagnosis)
admin.site.register(Session)

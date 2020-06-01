from django.contrib import admin
from .models import Medication, Diagnosis, Session, BloodTest, BloodTestRequest

admin.site.register(Medication)
admin.site.register(Diagnosis)
admin.site.register(Session)
admin.site.register(BloodTest)
admin.site.register(BloodTestRequest)

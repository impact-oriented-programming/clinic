from django.contrib import admin
from .models import Medication, Diagnosis, Session, BloodTest, BloodTestRequest
global db_counter
db_counter = 0




class Custoimize_Medication(admin.ModelAdmin):
    list_display = ('__str__', 'medication_code', 'medication_details', 'prescription_required' )

class Custoimize_Diagnosis(admin.ModelAdmin):
    list_display = ('__str__', 'diagnosis_code' )

class Custoimize_Sessions(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'time', 'chief_complaint', )
    list_filter = ['doctor', 'patient']

class Custoimize_BloodTest(admin.ModelAdmin):
    list_display = ('blood_test', 'blood_test_code' )

class Custoimize_BloodTestRequest(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'time' )

admin.site.register(Medication, Custoimize_Medication)
admin.site.register(Diagnosis, Custoimize_Diagnosis)
admin.site.register(Session, Custoimize_Sessions)
admin.site.register(BloodTest, Custoimize_BloodTest)
admin.site.register(BloodTestRequest, Custoimize_BloodTestRequest)


    

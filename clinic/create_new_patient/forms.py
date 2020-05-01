from django.forms import ModelForm
import general_models.models as gm

class CreatePatientForm(ModelForm):
    class Meta:
        model = gm.Patient
        fields = '__all__'


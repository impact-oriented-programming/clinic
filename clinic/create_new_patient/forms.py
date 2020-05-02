from django import forms
from django.forms import ModelForm
import general_models.models as gm
import pycountry
import datetime


class CreatePatientForm(ModelForm):
    origin_country = forms.ChoiceField(
        choices = sorted(((country.name, country.name) for country in pycountry.countries)),
        widget=forms.Select,
        required = True)

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years = list(range(datetime.datetime.now().year, 1900, -1))),
        required= True
    )

    gender = forms.ChoiceField(
        choices=(("f", "f"), ("m", "m")),
        widget=forms.Select,
        required=True
    )



    class Meta:
        model = gm.Patient
        fields = '__all__'


from django import forms


class CreatePatientForm(forms.form):
    first_name = forms.CharField(label='Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    gender = forms.CharField(label='Gender', max_length=30)
    language = forms.CharField(label='Language', max_length=30)
    phone_number = forms.CharField(label='Phone Number', max_length=30)
    email = forms.CharField(label='Email', max_length=30)
    origin_country = forms.CharField(label='Origin Country', max_length=30)
    date_of_birth = forms.CharField(label='Date of Birth', max_length=30)
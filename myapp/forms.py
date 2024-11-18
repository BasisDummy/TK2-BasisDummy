from django import forms
from .database import workers_db

class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    gender = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], required=True)
    phone = forms.CharField(max_length=15, required=True)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2023)), required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

class WorkerRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    phone = forms.CharField(max_length=15)
    dob = forms.DateField()
    address = forms.CharField(widget=forms.Textarea)
    account_number = forms.CharField(max_length=20)
    npwp = forms.CharField(max_length=20)
    photo_url = forms.CharField()
    bank_name = forms.ChoiceField(choices=[
        ('gopay', 'Gopay'),
        ('ovo', 'OVO'),
        ('bca', 'Virtual Account BCA'),
        ('bni', 'Virtual Account BNI'),
        ('mandiri', 'Virtual Account Mandiri'),
    ])

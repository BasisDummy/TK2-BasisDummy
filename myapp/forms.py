from django import forms
from .database import workers_db
from .models import Worker, User

class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    gender = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], required=True)
    phone = forms.CharField(max_length=15, required=True)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2023)), required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    
    # Validasi di level form
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Nomor HP sudah digunakan.')
        return phone
    
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
    # Validasi di level form
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Worker.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Nomor HP sudah digunakan.')
        return phone

    def clean_account_number(self):
        bank_name = self.cleaned_data.get('bank_name')
        account_number = self.cleaned_data.get('account_number')
        if Worker.objects.filter(bank_name=bank_name, account_number=account_number).exists():
            raise forms.ValidationError('Bank dan nomor rekening sudah terdaftar.')
        return account_number

    def clean_npwp(self):
        npwp = self.cleaned_data['npwp']
        if Worker.objects.filter(npwp=npwp).exists():
            raise forms.ValidationError('Nomor NPWP sudah digunakan.')
        return npwp
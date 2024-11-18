from django.db import models

class User(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)

    @classmethod
    def user_exists(cls, phone):
        return cls.objects.filter(phone=phone).exists()

    @classmethod
    def add_user(cls, data):
        cls.objects.create(**data)

    @classmethod
    def get_user_by_phone_and_password(cls, phone, password):
        return cls.objects.filter(phone=phone, password=password).first()

class Worker(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    phone = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    npwp = models.CharField(max_length=20)
    photo_url = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=50)

    @classmethod
    def worker_exists(cls, phone, npwp):
        return cls.objects.filter(phone=phone).exists() or cls.objects.filter(npwp=npwp).exists()
from django.urls import path
from .views import buat_testimoni, daftar_diskon, beli_voucher, daftar_testimoni

app_name = 'feat_3_blue'

urlpatterns = [
    path('buat-testimoni/<int:order_id>/', buat_testimoni, name='buat_testimoni'),
    path('daftar-testimoni/', daftar_testimoni, name='daftar_testimoni'),
    path('daftar-diskon/', daftar_diskon, name='daftar_diskon'),
    path('beli-voucher/<int:voucher_id>/', beli_voucher, name='beli_voucher'),
]
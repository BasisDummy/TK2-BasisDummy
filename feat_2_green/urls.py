from django.urls import path
from feat_2_green.views import *
app_name = 'feat_2_green'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('subkategori/<uuid:subcategory_id>/', subkategori, name='subkategori'),  
    path('pemesanan/<uuid:subkategori_id>/', buat_pemesanan, name='buat_pemesanan'),
    path('daftar-pesanan/', daftar_pesanan, name='daftar_pesanan'),
]
# mypay/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mypay_view, name='mypay_view'),
    path('transaksi/', views.transaksi_mypay_view, name='transaksi_mypay'),
]

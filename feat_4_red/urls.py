# feat_4_red/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.mypay_view, name='mypay_view'),
    path('transaksi/', views.transaksi_mypay_view, name='transaksi_mypay'),
    path('pekerjaan_jasa/', views.pekerjaan_jasa_view, name='pekerjaan_jasa'),
    path('accept_job/', views.accept_job_view, name='accept_job'),
    path('status_pekerjaan_jasa/', views.status_pekerjaan_jasa_view, name='status_pekerjaan_jasa'),
    path('update_job_status/', views.update_job_status_view, name='update_job_status'),
]

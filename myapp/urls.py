from django.urls import path
from .views import choose_role, register_user, register_worker, login, home_user, home_worker, logout, landing

urlpatterns = [
    path('', landing, name='landing'),
    path('register/user/', register_user, name='register_user'),
    path('register/worker/', register_worker, name='register_worker'),
    path('login/', login, name='login'),
    path('home/user/', home_user, name='home_user'),
    path('home/worker/', home_worker, name='home_worker'),
    path('logout/', logout, name='logout'),
    path('choose_role/', choose_role, name='choose_role'),
]
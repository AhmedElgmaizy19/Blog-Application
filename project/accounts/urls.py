from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('changepassword/', change_password, name='changepassword'),
    path('profile/<int:pk>', user_profile, name='profile'),
]

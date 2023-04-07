from django.urls import path
from .views import personal_cabinet, login, register

urlpatterns = [
    path('', personal_cabinet, name='personal_cabinet'),
    path('login/', login, name='login'),
    path('register/', register, name='register')
]

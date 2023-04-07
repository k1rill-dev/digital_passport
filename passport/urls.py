from django.urls import path
from .views import personal_cabinet, register, logout_user, add_personal_data, get_biometrical_data

urlpatterns = [
    path('', personal_cabinet, name='personal_cabinet'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('add_personal_data/', add_personal_data, name='add_personal_data'),
    path('get_biometrical_data/', get_biometrical_data, name='get_biometrical_data')
]

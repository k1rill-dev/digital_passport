from django.urls import path
from .views import personal_cabinet, register, logout_user, add_personal_data, get_biometrical_data, login_with_otp, \
    send_otp, login_with_biometria

urlpatterns = [
    path('', personal_cabinet, name='personal_cabinet'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_with_otp, name='login_with_otp'),
    path('twofa_auth/', send_otp, name='send_otp'),
    path('login_with_biometria/', login_with_biometria, name='login_with_biometria'),
    path('add_personal_data/', add_personal_data, name='add_personal_data'),
    path('get_biometrical_data/', get_biometrical_data, name='get_biometrical_data')
]

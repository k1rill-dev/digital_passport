from django.urls import path
from .views import personal_cabinet, logout_user, add_personal_data, login_biometrical_data, login_with_otp, \
    send_otp, add_biometria, check_blockchain, index

urlpatterns = [
    path('lk/', personal_cabinet, name='personal_cabinet'),
    path('', index, name='index'),
    path('logout/', logout_user, name='logout'),
    path('check_blockchain/', check_blockchain, name='check_blockchain'),
    path('login/', login_with_otp, name='login_with_otp'),
    path('twofa_auth/', send_otp, name='send_otp'),
    path('add_personal_data/', add_personal_data, name='add_personal_data'),
    path('add_biometria/', add_biometria, name='add_biometria'),
    path('login_biometrical_data/', login_biometrical_data, name='login_biometrical_data')
]

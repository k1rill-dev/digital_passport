import ast
import io
import json
from PIL import Image
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from .forms import UpdatePersonalInfoForm, CreateUserForm
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from social_django.utils import psa
from .models import User
import pyotp
from django.core.mail import send_mail

otp_dict = {}
otp_secret = {}


@psa('social:complete')
def auth(request, backend):
    backend = request.strategy.backend
    try:
        user = backend.do_auth(request.user.email)
    except:
        user = None
    if user is not None and user.is_active:
        # login(request, user)
        print('=======================================================================')
        return redirect(reverse('get_biometrical_data'))
    else:
        messages.error(request, 'Ошибка авторизации')
        print('=======================================================================')
        return redirect(reverse('login'))


@login_required
def personal_cabinet(request):
    return render(request, 'passport/personal_cabinet.html')


def index(request):
    return render(request, 'passport/index.html')


def logout_user(request):
    logout(request)
    return redirect('personal_cabinet')


def add_personal_data(request):
    if request.method == 'POST':
        form = UpdatePersonalInfoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_instance = User.objects.get(pk=request.user.pk)
            if user_instance.email is None:
                user_instance.email = cd['email']
            user_instance.date_of_birthday = cd['date_of_birthday']
            user_instance.number_of_phone = cd['number_of_phone']
            user_instance.set_password(cd['password'])
            user_instance.city = cd['city']
            user_instance.address = cd['address']
            user_instance.save()
            return redirect('personal_cabinet')
    else:
        form = UpdatePersonalInfoForm()
        return render(request, 'passport/add_personal_data.html', {'form': form})


def send_otp(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            cd = form.cleaned_data
            confirm_password = cd.pop('confirm_password')

            if cd['password'] == confirm_password:
                user = User.objects.create_user(**cd)

            key = otp_secret.get(cd['email'], None)
            if key is None:
                key = pyotp.random_base32(40)

            print(key)
            totp = pyotp.TOTP(key, interval=300)
            token = totp.now()
            print(token)

            otp_dict[cd['email']] = token

            subject = 'Одноразовый токен для входа в систему'
            message = f'Ваш одноразовый токен для входа в систему: {token}'

            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['email']])

            return redirect('login_with_otp')
        else:
            return HttpResponse('не слава мэрлоу')
    else:
        form = CreateUserForm()
        return render(request, 'passport/expire_email.html', {'form': form})


def login_with_otp(request):
    if request.method == 'POST':
        token = int(
            f'{request.POST["t1"]}{request.POST["t2"]}{request.POST["t3"]}{request.POST["t4"]}{request.POST["t5"]}{request.POST["t6"]}')
        if token in otp_dict.values():
            email = next(ch for ch, code in otp_dict.items() if code == token)
            login(request, User.objects.get(email=email), backend='django.contrib.auth.backends.ModelBackend')
            otp_dict.pop(email)
            print(otp_dict)
            return redirect('personal_cabinet')
        else:
            return HttpResponse('Invalid token.')
    else:
        return render(request, 'passport/confirm_code.html')


@csrf_exempt
def get_biometrical_data(request):
    if request.method == 'POST':
        data = ast.literal_eval(request.body.decode('utf-8'))
        with open('img.jpeg', 'wb') as f:
            f.write(base64.b64decode(data['img'].replace('data:image/jpeg;base64,', '')))
    return render(request, 'passport/biometrica.html')


def login_with_biometria(request):
    if request.method == 'POST':
        print(request.POST)
    return HttpResponse('опа опа опа биометрия')

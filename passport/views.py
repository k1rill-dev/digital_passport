import ast
import io
import json
import os

from .utils import *
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
from .blockchain import get_hash, _check_blockchain
from .RSA_AES import Aes
from requests import get, post
from datetime import date
import datetime
from dateutil import relativedelta

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
    data = User.objects.get(pk=request.user.pk)
    aes = Aes()
    key = get(f'http://127.0.0.1:5000/get_key/{request.user.pk}').json()['key']

    today = date.today()
    birthday = datetime.datetime.strptime(aes.dec_aes(data.date_of_birthday, key[0]), '%d.%m.%Y')
    date_diff = relativedelta.relativedelta(today, birthday)
    years = date_diff.years  # 23
    blocks = User.objects.all()

    dict_data = {
        'date_of_birthday': aes.dec_aes(data.date_of_birthday, key[0]),
        'number_of_phone': aes.dec_aes(data.number_of_phone, key[0]),
        'city': aes.dec_aes(data.city, key[0]),
        'address': aes.dec_aes(data.address, key[0]),
        'last_login': data.last_login,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'email': data.email,
        'data_joined': data.date_joined,
        'years': years,
        'hash': data._hash,
        'check': _check_blockchain(blocks)
    }

    return render(request, 'passport/personal_cabinet.html', {'dict_data': dict_data})


def index(request):
    return render(request, 'passport/index.html')


def logout_user(request):
    logout(request)
    return redirect('personal_cabinet')


def add_personal_data(request):
    if request.method == 'POST':
        form = UpdatePersonalInfoForm(request.POST)
        if form.is_valid():
            data = ast.literal_eval(request.body.decode('utf-8'))
            with open('img.jpeg', 'wb') as f:
                f.write(base64.b64decode(data['img'].replace('data:image/jpeg;base64,', '')))
            cd = form.cleaned_data
            aes = Aes()
            key_aes = aes.print_key()
            user_instance = User.objects.get(pk=request.user.pk)
            user_previous = User.objects.all().order_by('-id')[1]
            if user_instance.email is None:
                user_instance.email = cd['email']
            user_instance.set_password(cd['password'])

            date_of_birthday = aes.enc_aes(str(cd['date_of_birthday']))
            number_of_phone = aes.enc_aes(str(cd['number_of_phone']))
            city = aes.enc_aes(cd['city'])
            address = aes.enc_aes(cd['address'])
            user_instance.date_of_birthday = date_of_birthday
            user_instance.number_of_phone = number_of_phone
            user_instance.city = city
            user_instance.address = address

            # ЗАМЕНИТЬ НА ПОЛУЧЕНИЕ КЛЮЧА ИЗ ДРУГОЙ БАЗЫ
            post('http://127.0.0.1:5000/post_key', json={'id': request.user.pk, 'key': key_aes})
            # user_instance.temporary_field_key_aes = key_aes

            user_instance._hash = get_hash(date_of_birthday, number_of_phone, city, address,
                                           user_previous._hash)
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

                aes = Aes()
                user_previous = User.objects.all().order_by('-id')[0]

                date_of_birthday = aes.enc_aes(str(cd['date_of_birthday']))
                number_of_phone = aes.enc_aes(str(cd['number_of_phone']))
                city = aes.enc_aes(cd['city'])
                address = aes.enc_aes(cd['address'])
                # ЗАМЕНИТЬ НА ПОЛУЧЕНИЕ КЛЮЧА ИЗ ДРУГОЙ БАЗЫ
                post('http://127.0.0.1:5000/post_key', json={'id': user_previous.pk + 1, 'key': aes.print_key()})
                # # user_instance.temporary_field_key_aes = key_aes
                #
                # user_instance._hash = get_hash(date_of_birthday, number_of_phone, city, address,
                #                                user_previous._hash)
                #
                print(cd)
                user = User.objects.create_user(
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    password=cd['password'],
                    email=cd['email'],
                    number_of_phone=number_of_phone,
                    date_of_birthday=date_of_birthday,
                    city=city,
                    address=address,
                    username=cd['username'],
                    _hash=get_hash(date_of_birthday, number_of_phone, city, address, user_previous._hash)
                )
            else:
                print('ты дибил пароли не совпали.......................................................')
            key = otp_secret.get(cd['email'], None)
            if key is None:
                key = pyotp.random_base32(40)

            totp = pyotp.TOTP(key, interval=300)
            token = totp.now()

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
        token = (
            f'{request.POST["t1"]}{request.POST["t2"]}{request.POST["t3"]}{request.POST["t4"]}{request.POST["t5"]}{request.POST["t6"]}')
        if token in otp_dict.values():
            email = next(ch for ch, code in otp_dict.items() if code == token)
            login(request, User.objects.get(email=email), backend='django.contrib.auth.backends.ModelBackend')
            otp_dict.pop(email)
            return redirect('personal_cabinet')
        else:
            return HttpResponse('Invalid token.')
    else:
        return render(request, 'passport/confirm_code.html')


@csrf_exempt
def login_biometrical_data(request):
    if request.method == 'POST':
        data = ast.literal_eval(request.body.decode('utf-8'))
        with open('img.jpeg', 'wb') as f:
            f.write(base64.b64decode(data['img'].replace('data:image/jpeg;base64,', '')))
        user = User.objects.get(pk=request.user.pk)
        with open(f'{user.username}.jpeg', 'wb') as f:
            f.write(user.face)
        print(find_difference('img.jpeg', f'{user.username}.jpeg'))
    return render(request, 'passport/biometrica.html')

@csrf_exempt
def add_biometria(request):
    if request.method == 'POST':
        data = ast.literal_eval(request.body.decode('utf-8'))
        with open(f'{request.user.username}.jpeg', 'wb') as f:
            f.write(base64.b64decode(data['img'].replace('data:image/jpeg;base64,', '')))
        photo_format(f'{request.user.username}.jpeg')
        with open(f'{request.user.username}cropped.jpeg', 'rb') as f:
            data = f.read()
        os.remove(f'{request.user.username}.jpeg')
        os.remove(f'{request.user.username}cropped.jpeg')
        user = User.objects.get(pk=request.user.pk)
        user.face = base64.b64encode(data).decode()
        user.save()
    return render(request, 'passport/biometrica.html', {'add': True})


def check_blockchain(request):
    blocks = User.objects.all()
    # change_block
    # for i in range(1, len(blocks)):
    #     currentBlock = blocks[i]
    #     prevBlock = blocks[i - 1]
    #
    #     if (get_hash(currentBlock.date_of_birthday, currentBlock.number_of_phone, currentBlock.city,
    #                  currentBlock.address, prevBlock._hash) != currentBlock._hash):
    #         return False, currentBlock
    #
    # return True

    response = _check_blockchain(blocks)

    return HttpResponse(response)

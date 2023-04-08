from django.conf import settings
from django.http import HttpResponse
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


def register(request):
    return render(request, 'passport/register.html')


def logout_user(request):
    logout(request)
    return redirect('personal_cabinet')


def add_personal_data(request):
    if request.method == 'POST':
        form = UpdatePersonalInfoForm(request.POST)
        if form.is_valid():
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
            user_instance.temporary_field_key_aes = key_aes

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
        form = CreateUserForm()
        return render(request, 'passport/expire_email.html', {'form': form})


def login_with_otp(request):
    if request.method == 'POST':
        token = request.POST.get('token')
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


def get_biometrical_data(request):
    if request.method == 'POST':
        ...
    return render(request, 'passport/get_biometria.html')


def login_with_biometria(request):
    ...


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

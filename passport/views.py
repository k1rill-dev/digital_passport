from .forms import UpdatePersonalInfoForm
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from social_django.utils import psa
from .models import User


@psa('social:complete')
def auth(request, backend):
    backend = request.strategy.backend
    try:
        user = request.backend.do_auth(request.user.email)
    except:
        user = None
    if user is not None and user.is_active:
        login(request, user)
        print('=======================================================================')
        return redirect(reverse('profile'))
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
            user_instance = User.objects.get(pk=request.user.pk)
            if user_instance.email is None:
                user_instance.email = cd['email']
            user_instance.date_of_birthday = cd['date_of_birthday']
            user_instance.number_of_phone = cd['number_of_phone']
            user_instance.set_password(cd['password'])
            user_instance.city = cd['city']
            user_instance.address = cd['address']
            user_instance.save()
            return redirect('get_biometrical_data')
        else:
            return render(request, 'passport/add_personal_data.html')
    else:
        form = UpdatePersonalInfoForm()
        return render(request, 'passport/add_personal_data.html', {'form': form})


def get_biometrical_data(request):
    if request.method == 'POST':
        ...
    return render(request, 'passport/get_biometria.html')

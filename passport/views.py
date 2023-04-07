from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# @login_required
def personal_cabinet(request):
    return render(request, 'passport/personal_cabinet.html')


def login(request):
    return render(request, 'passport/login.html')


def register(request):
    return render(request, 'passport/register.html')

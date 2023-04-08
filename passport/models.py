from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    face = models.ImageField(upload_to='face_of_user/%Y/%m/%d/', blank=True, null=True, verbose_name='Лицо')
    date_of_birthday = models.CharField(max_length=15, verbose_name='Дата рождения', blank=True, null=True, )
    city = models.CharField(max_length=100, verbose_name='Город проживания', blank=True, null=True, )
    address = models.CharField(max_length=255, verbose_name='Адрес проживания', blank=True, null=True, )
    number_of_phone = models.CharField(max_length=50, verbose_name='Номер телфона', blank=True, null=True, )
    _hash = models.CharField(max_length=200, verbose_name='Хэш предыдущего блока', blank=True, null=True, )
    temporary_field_key_aes = models.CharField(max_length=200, verbose_name='key', blank=True, null=True, )

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    face = models.ImageField(upload_to='face_of_user/%Y/%m/%d/', blank=True, null=True,
                             default='Нет картинки',
                             verbose_name='Лицо')
    date_of_birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True, )
    city = models.CharField(max_length=100, verbose_name='Город проживания', blank=True, null=True, )
    address = models.CharField(max_length=255, verbose_name='Адрес проживания', blank=True, null=True, )
    number_of_phone = models.IntegerField(max_length=11, verbose_name='Номер телфона', blank=True, null=True, )

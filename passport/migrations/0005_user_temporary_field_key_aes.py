# Generated by Django 4.1.3 on 2023-04-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport', '0004_user_perv_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='temporary_field_key_aes',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='key'),
        ),
    ]
# Generated by Django 4.1.2 on 2022-10-28 16:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_about_account_phone_account_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписки'),
        ),
    ]
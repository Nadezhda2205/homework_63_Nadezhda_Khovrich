# Generated by Django 4.1.2 on 2022-10-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_account_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(default=1, upload_to='avatars'),
            preserve_default=False,
        ),
    ]

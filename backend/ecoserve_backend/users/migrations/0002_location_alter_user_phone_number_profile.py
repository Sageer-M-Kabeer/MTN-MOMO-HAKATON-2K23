# Generated by Django 4.2.6 on 2023-10-23 12:24

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('NGIGERIA', 'Ngigeria'), ('GHANA', 'Ghana')], max_length=10)),
                ('state', models.CharField(choices=[('ABJ', 'Abuja'), ('KN', 'Kano'), ('LG', 'Lagos')], max_length=10)),
                ('city', models.CharField(choices=[], max_length=10)),
                ('address', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(error_messages={'unique': 'A user with that phone number already exists.'}, max_length=11, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+\\d{12}$')]),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peofile_id', models.CharField(max_length=16)),
                ('username', models.CharField(max_length=25, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

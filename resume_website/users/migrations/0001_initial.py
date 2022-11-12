# Generated by Django 4.1.3 on 2022-11-12 14:28

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='Male', max_length=10, null=True, verbose_name='Gender')),
                ('country', django_countries.fields.CountryField(default='', max_length=2)),
                ('featured_img', models.ImageField(default='profiles/profile_default.jpg', upload_to='profiles', verbose_name='A profile image')),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('is_stuff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'ordering': ['email'],
            },
        ),
    ]

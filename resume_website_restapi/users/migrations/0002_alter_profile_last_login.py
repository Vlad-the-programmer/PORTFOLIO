# Generated by Django 4.1.3 on 2022-12-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Last logged in'),
        ),
    ]

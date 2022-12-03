# Generated by Django 4.1.3 on 2022-12-03 12:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=100, message='Title is over 100 letters long!')])),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('content', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='comments')),
            ],
            options={
                'verbose_name': 'Comments',
                'verbose_name_plural': 'Comments',
                'ordering': ['-date_created'],
            },
        ),
    ]
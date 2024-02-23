# Generated by Django 5.0.2 on 2024-02-23 15:56

import django.core.validators
import re
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField(blank=True, max_length=500, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=100, message='Comment is over 500 letters long!')])),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid'), django.core.validators.MaxLengthValidator(limit_value=100, message='Slug is over 100 letters long!')])),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.MaxLengthValidator(limit_value=100, message='Title is over 100 letters long!')])),
                ('image', models.ImageField(blank=True, null=True, upload_to='comments/<django.db.models.fields.SlugField>')),
                ('disabled', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'verbose_name': 'Comments',
                'verbose_name_plural': 'Comments',
                'ordering': ['-date_created'],
            },
        ),
    ]
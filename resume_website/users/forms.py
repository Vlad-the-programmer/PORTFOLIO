from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'slug')

        
class UserCreateForm(UserCreationForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'slug', 'tags')
        # widgets = {
        #     'tags': {''}
        # }
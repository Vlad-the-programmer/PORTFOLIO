from django import forms
from django.db import models
from .models import Post


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'slug')
        

class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'slug', 'tags', 'category')
        # widgets = {'tags': forms.MultipleChoiceField()}
        
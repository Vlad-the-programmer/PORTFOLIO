from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.widgets import CountrySelectWidget
from .models import Profile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'country',
                  'featured_img',
                  'gender',
                  )
        exclude = ['password']

        
class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Profile
        fields = (
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'country',
                  'featured_img',
                  'gender',
                )
        widgets = {'country': CountrySelectWidget()}
        
class UserLoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'password')
        widgets = {'password': forms.PasswordInput}
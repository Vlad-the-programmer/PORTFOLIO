from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.widgets import CountrySelectWidget
from allauth.account import forms as login_form

from .models import Profile

class UserUpdateForm(UserChangeForm):
    featured_img = forms.ImageField(required=False)
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
        
class UserLoginForm(login_form.LoginForm):
    class Meta:
        def __init__(self):
            super(login_form.LoginForm, self).__init__()
            for field in self.fields:
                field.update({'class': 'form-control'})
        

class UserPasswordResetForm(forms.ModelForm):
    confirm_password = forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    class Meta:
        model = Profile
        fields = ('password',)
        widgets = {'password': forms.PasswordInput(attrs={'placeholder': 'New password'})}
        
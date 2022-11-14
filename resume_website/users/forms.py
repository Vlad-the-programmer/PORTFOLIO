from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.widgets import CountrySelectWidget
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
        # def __init__(self):
        #     self.featured_img.widget.attrs.update({'required': False})

        
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
        

class UserPasswordResetForm(forms.ModelForm):
    confirm_password = forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    class Meta:
        model = Profile
        fields = ('password',)
        widgets = {'password': forms.PasswordInput(attrs={'placeholder': 'New password'})}
        
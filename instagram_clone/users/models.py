from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

import uuid

from .managers import UserManager


class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
    OTHER = "other", _("Other")


class Profile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    id = models.AutoField(primary_key=True)
    email = models.EmailField(  
                              unique=True, 
                              blank=True,
                              null=True, 
                              max_length=254,
                              validators=[
                                            validators.EmailValidator()
                                        ])
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
                                _('Gender'),
                                max_length=10,
                                choices=Gender.choices,
                                default=_('Male'),
                                null=True)
    country = CountryField(
                            blank_label=_('(select country)'),
                            default='',
                            max_length=50,
                        )
    followed_by = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='following_users',
                                    blank=True, 
                                    null=True
                                )
    following = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='follower',
                                    blank=True,
                                    null=True
                                )   
    password = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(
                                    unique=True, 
                                    max_length=100, 
                                    blank=True, 
                                    null=True
                                )
    featured_img = models.ImageField(
                                        verbose_name=_('A profile image'),
                                        upload_to=f'profiles/{username}', 
                                        default='profiles/profile_default.jpg'
                                    )
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(
                                        _('Last logged in'),
                                        null=True, 
                                        blank=True
                                    )
    is_staff = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    is_superuser = models.BooleanField(default=False, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.followed_by.username} is following {self.following.username}"
        
    def set_username(self):
        return self.email.split('@')[0].lower()
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_add_permission(request):
        if request.user.is_authenticated:
            return True
        return False

    def has_change_permission(request):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_delete_permission(request):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_module_perms(self, app_label):
        return True
    
    def get_user_perms(self):
        return {    
                    'add': self.has_add_permission(),
                    'change': self.has_change_permission(),
                    'delete': self.has_delete_permission()
                }
        
    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = get_object_or_404(cls.__class__, email__exact=email)
        except:
            user = None
        if user is not None:
            return True
        return False  
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def imageURL(self):
        try:
            url = self.featured_img.url
        except:
            url = ''
        return url

    def is_following(self):
        if self is None:
            return None
        return self.following.filter(id=self.id)
    
    def is_followed_by(self):
        if self is None:
            return None
        return self.followed_by.filter(id=self.id)
    
    class Meta:
       verbose_name = _('User')
       verbose_name_plural = _('Users')
       ordering = ['email']
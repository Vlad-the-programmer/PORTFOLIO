from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from .managers import UserManager

class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
    OTHER = "other", _("Other")


class Profile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    email = models.EmailField(unique=True, 
                              blank=True,
                              null=True, 
                              validators=[
                                            validators.EmailValidator()
                                        ])
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(_('Gender'),
                              max_length=10,
                              choices=Gender.choices,
                              default=_('Male'),
                              null=True)
    country = CountryField(blank_label=_('(select country)'), default='')
    featured_img = models.ImageField(verbose_name=_('A profile image'),
                                     upload_to='profiles', 
                                     default='profiles/profile_default.jpg')
    password = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    is_stuff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
    def exists(self):
        email = self.email
        try:
            user = Profile.objects.get(email=email)
        except:
            user = None
        if user is not None:
            return True
        return False 
    
    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
        except:
            user = None
        if user is not None:
            return True
        return False 
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.username
    
    @property
    def imageURL(self):
        try:
            url = self.featured_img.url
        except:
            url = ''
        return url

    class Meta:
       verbose_name_plural = 'Users'
       ordering = ['email']
    
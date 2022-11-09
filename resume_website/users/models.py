from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    # USERNAME_FIELD = ''
    # REQUIRED_FIELDS = []
    
    user = models.OneToOneField(User,
                                related_name='profile', 
                                on_delete=models.CASCADE)
    # email = models.EmailField(blank=True)
    # class Meta(User.Meta):
       
    
    def __str__(self):
        return self.user.email
    

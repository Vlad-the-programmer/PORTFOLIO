import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_slug, MaxLengthValidator

class Post(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    title = models.CharField(unique=True,
                             max_length=100,
                             validators=[
                                  MaxLengthValidator(
                                    limit_value=100,
                                    message="Slug is over 100 letters long!"
                                    )
                                ]
                             )
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="default.jpg")
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            blank=True,
                            null=True,
                            validators=[
                                validate_slug, 
                                MaxLengthValidator(
                                    limit_value=100,
                                    message="Slug is over 100 letters long!"
                                    )
                                ]
                            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tags', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='profile',
                             on_delete=models.CASCADE)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['title']

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return 
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        
class Tags(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    title = models.CharField(max_length=200,
                             validators=[
                              MaxLengthValidator(
                                    limit_value=200,
                                    message="Slug is over 100 letters long!"
                                    )
                                ]
                             )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        
class Category(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.slug
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
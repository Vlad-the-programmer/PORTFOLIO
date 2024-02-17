from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator, validate_slug
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid


class STATUS(models.TextChoices):
    SENT = "sent", _("Sent")
    UNSENT = "unsent", _("Unsent")
    
    
class Chat(models.Model):
    id = models.UUIDField(  
                            default=uuid.uuid4, 
                            unique=True,
                            primary_key=True, 
                            editable=False
                        )
    slug = models.SlugField(
                            max_length=100, 
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
    author = models.ForeignKey( 
                                settings.AUTH_USER_MODEL,
                                related_name='chat',
                                on_delete=models.CASCADE
                            )
    chat_to_user = models.ForeignKey(   
                                        settings.AUTH_USER_MODEL,
                                        related_name='foreign_chat',
                                        on_delete=models.CASCADE
                                    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")
        ordering = ['-date_created']
        
    def __str__(self):
        return self.slug
        
    def set_slug(self):
        self.slug = slugify(str(self.id) + "-from-" + self.author.username  \
                                     + "-to-" + self.chat_to_user.username )
        
    def get_absolute_url(self):
        return reverse('messages:chat-detail', kwargs={'chat_slug': self.slug})
    
    
class Message(models.Model):
    id = models.UUIDField(  
                            default=uuid.uuid4, 
                            unique=True,
                            primary_key=True, 
                            editable=False
                        )
    message = models.TextField(
                            max_length=500,
                            blank=True, 
                            null=True,
                            validators=[
                                MaxLengthValidator(
                                    limit_value=100,
                                    message="Message is over 500 letters long!"
                                )
                            ]
                        )
    chat = models.ManyToOneRel( 
                               'messages.Chat',
                                related_name = 'messages',
                                on_delete=models.CASCADE
                            )
    author = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                related_name='chat',
                                on_delete=models.CASCADE
                            )
    sent_for = models.ForeignKey(  
                                    settings.AUTH_USER_MODEL,
                                    related_name='chat',
                                    on_delete=models.CASCADE
                                )
    status = models.CharField(  
                                _('Status'),
                                max_length=10,
                                choices=STATUS,
                                default=STATUS.SENT,
                                blank=True, 
                                null=True
                            )
    image = models.ImageField(  
                                null=True, 
                                blank=True, 
                                upload_to=f'chats/{chat.slug}'
                            )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = _("Messages")
        verbose_name_plural = _("Messages")
        ordering = ['-date_created']
        
    def __str__(self):
        return self.id + " " + self.author.username
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return 
        
        
    def get_absolute_url(self):
        return reverse('messages:chat-detail', kwargs={'chat_slug': self.chat.slug})
    
    
    
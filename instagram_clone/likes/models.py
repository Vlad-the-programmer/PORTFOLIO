from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class Like(models.Model):
    id = models.UUIDField(  
                            default=uuid.uuid4, 
                            unique=True,
                            primary_key=True, 
                            editable=False
                        )
    author = models.ForeignKey( 
                                settings.AUTH_USER_MODEL,
                                related_name='given_likes',
                                on_delete=models.CASCADE
                            )
    post = models.ForeignKey( 
                                "posts.Post",
                                related_name='likes',
                                on_delete=models.CASCADE
                            )
    timestamp =  models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"For post: {self.post.slug} given by {self.author.username}"


    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        ordering = ['-timestamp']
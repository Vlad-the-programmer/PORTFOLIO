from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from common.models import TimeStampedUUIDModel


class Like(TimeStampedUUIDModel):
    author = models.ForeignKey( 
                                settings.AUTH_USER_MODEL,
                                related_name='given_likes',
                                on_delete=models.CASCADE
                            )
    post = models.ForeignKey( 
                                "posts.Post",
                                related_name='post_likes',
                                on_delete=models.CASCADE
                            )
    
    
    def __str__(self):
        return f"For post: {self.post.slug} given by {self.author.username}"


    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        ordering = ['-created_at']
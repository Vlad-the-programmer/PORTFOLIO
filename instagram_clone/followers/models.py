from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimeStampedUUIDModel


User = get_user_model()


class UserFollowing(TimeStampedUUIDModel):

    user = models.ForeignKey(    
                                User, 
                                related_name="following", 
                                on_delete=models.CASCADE
                            )
    following_user = models.ForeignKey(  
                                          User, 
                                          related_name="followers",
                                          on_delete=models.CASCADE
                                        )

    class Meta:
        constraints = [
            models.UniqueConstraint(    
                                    fields=['user_id','following_user_id'],
                                    name="unique_followers"
                                )
        ]

        ordering = ["-created_at"]

    def __str__(self):
        f"{self.user_id} follows {self.following_user_id}"
        
        
    def has_chat_to_user_perms(self, request, user_to_chat_id):
        if request.user.is_authenticated \
                            and self.following_user_id == user_to_chat_id:
            return True
        return False
    
    

import logging
from django.db.models.base import Model as Model
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import detail, edit

from .models import UserFollowing

logger = logging.getLogger(__name__)

Profile = get_user_model()


def followUser(request, username):
    user = Profile.objects.filter(username=username).first()
    if not user:
        messages.info(request, "User not found!")
        return redirect(redirect_url)
    
    redirect_url = reverse('users:profile-detail', kwargs={
                                                            'pk': user.id
                                                        }
                              )
    current_user = request.user
    
    
    if user.username == current_user.username:
        messages.info(request, "You cannot follow yourself!")
        return redirect(redirect_url)
    else:
        if current_user.following_users_list.filter(following_user_id__username=username).first():
            messages.info(request, "You follow the user already!")
            print("Follow!")
            return redirect(redirect_url) 
        else:
            followingUser = UserFollowing.objects.create(   
                                                user=current_user,
                                                following_user=user
                                            )
            current_user.following.add(followingUser)
            return redirect(redirect_url)

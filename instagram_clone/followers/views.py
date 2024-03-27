import logging
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.http import Http404
# Auth
from django.contrib.auth import get_user_model
from django.contrib import messages
# Generic class-based views
from django.contrib.auth.decorators import login_required
from django.views.generic import detail, edit

from .models import UserFollowing
from posts.models import Post
from common import mixins as common_mixins
from common import decorators as common_decorators


logger = logging.getLogger(__name__)

Profile = get_user_model()


@common_decorators.login_required
def followUser(request, username):
    user = Profile.objects.filter(username=username).first()
    
    currentUser = request.user
    is_following_user = currentUser.is_following(user.username)
    # is_following_user = UserFollowing.objects.filter(user=currentUser).filter(
    #             following_user=user
    #         ).exists()
    render_func = render(request, 
                          "followers/followerProfile_detail.html",
                          { 
                            'followingUser': user, 
                            'is_following': is_following_user,
                            'profile': currentUser
                        }
                    )
    if user is None:
        messages.info(request, "User not found!")
        return render_func
    
    print("is following ", is_following_user)
    print("User following list ", currentUser.following_users_list)
    
    
    if user.username == currentUser.username:
        messages.info(request, "You cannot follow yourself!")
        return render_func
    
    followingUser = currentUser.getFollowingUser(user.username)
    # followingUser = UserFollowing.objects.filter(user=currentUser).filter(
    #             following_user=user
    #         ).first()
    print('following user', followingUser)
    if followingUser is not None:
        messages.info(request, "You follow the user already!")
        print("Follow!")
        return render_func
    
    followingUser = UserFollowing.objects.create(   
                                        user=currentUser,
                                        following_user=user
                                    )
    # currentUser.following.add(followingUser)
    return render_func


@common_decorators.login_required
def unFollowUser(request, username):
    user = Profile.objects.filter(username=username).first()
    if user is None:
        messages.info(request, "User not found!")
        return render_func
    
    currentUser = request.user
    is_following_user = currentUser.is_following(user.username)
    # is_following_user = UserFollowing.objects.filter(user=currentUser).filter(
    #             following_user__username=username
    #         ).exists() 
    
    print("is following ", is_following_user)
    print("User following list ", currentUser.following_users_list)
    
    render_func = render(request, 
                          "followers/followerProfile_detail.html",
                          { 
                            'followingUser': user, 
                            'is_following': is_following_user,
                            'profile': currentUser
                        }
                    )
    
    if user.username == currentUser.username:
        messages.info(request, "You cannot follow yourself!")
        return render_func
    
    followingUser = currentUser.getFollowingUser(user.username)
    # followingUser = UserFollowing.objects.filter(user=currentUser).filter(
    #             following_user__username=username
    #         ).first()
    
    print('Unfollow-following user is', followingUser)
    if followingUser is not None:
        messages.info(request, "User unfollowed!")
        followingUser.delete()
        return render_func
    
    messages.info(request, "Your are not following the user!")
    return render_func


class FollowingProfileDetailView(common_mixins.LoginRequiredMixin,
                                 detail.DetailView
                                ):
    model = Profile
    template_name = "followers/followerProfile_detail.html"
    context_object_name = 'followingUser'
    pk_url_kwarg = 'username'
    
    
    def get_object(self):
        username_ = self.kwargs.get('username', '')
        
        try:
            profile = Profile.objects.filter(username=username_).first()
        except Profile.DoesNotExist:
            return Http404("User not found")
        return profile
    
import json
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Auth
from django.contrib.auth import get_user_model, logout
from allauth.account.utils import logout_on_password_change
# REST FRAMEWORK 
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics

from .serializers import (
                        UserRegisterSerializer, 
                        UserSerializer, 
                        PasswordResetSerializer,
                        ChangePasswordSerializer,
                    )

from . import exceptions as custom_exceptions


Profile = get_user_model()


class UserSignUpApiView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        
class UsersListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.AllowAny,)


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny,])
def activate_account(request, uuid, token):
    try:
        user = Profile.objects.get(id=uuid)
    except (Profile.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
    else:
        raise custom_exceptions.UserOrTokenNotValid
    
    return Response(
        {"200:Activated"},
        status=status.HTTP_200_OK,
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
def reset_password(request, *args, **kwargs):
    print('kwargs', kwargs)
    serializer = PasswordResetSerializer(
            data=request.data, 
            context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    
    return Response(
        {200: "Send an confirmation email"},
        status=status.HTTP_302_FOUND,
    )
    

class PasswordChangeApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.AllowAny,)
    
    
    def get_object(self):
        try:
            profile = Profile.objects.get(id=self.kwargs.get('uuid', ''))
        except Profile.DoesNotExist:
            profile = None
        
        return profile 
    

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(
                                            instance=user,
                                            data=request.data,
                                            partial=True,
                                            context={'request': self.request},
                                        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        logout_on_password_change(request, user)
        return Response(
            {'detail':'Password changed!'},
            status=status.HTTP_200_OK,
        )
        
        
class  ProfileDetailUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    
    
    def get_object(self):
        try:
            profile = Profile.objects.get(id=self.kwargs.get('pk', ''))
        except Profile.DoesNotExist:
            profile = None
        print(self.request.user, self.request.user.is_authenticated)
        print(self.request.user.auth_token)
        
        return profile 
    
    
    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile is not None:
            self.perform_destroy(profile)
            logout(request)
            return Response(
                {'detail': 'Profile deleted!'},
                status=status.HTTP_200_OK,
            )
            
        return Response(
                        {'detail': 'Profile does not exist!'},
                        status=status.HTTP_200_OK,
                    )
    

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def user_authenticated(request, *args, **kwargs):
    return Response(
        {'is_authenticated': request.user.is_authenticated, 'user': f'{request.user}'}
    )   
       

# the Logout dj-rest-auth view and this one do not work   
@api_view(["POST"])
def logout_user(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')
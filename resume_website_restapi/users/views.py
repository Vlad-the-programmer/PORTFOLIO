from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Auth
from django.contrib.auth import get_user_model
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

Profile = get_user_model()


class UserSignUpApiView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = ()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        
class UsersListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = Profile.objects.all()
    permission_classes = ()


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
        raise ValueError(_("User id or token is not valid!")) 
    
    return Response(
        {"200:Activated"},
        status=status.HTTP_200_OK,
        )


class PasswordChangeApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['POST', 'PUT', 'PATCH']
    
    def get_object(self):
        try:
            profile = Profile.objects.get(id=self.kwargs.get('uuid', ''))
        except Profile.DoesNotExist:
            profile = None
        
        return profile 
    
    
    def patch(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.serializer_class(
                                            instance=profile,
                                            data=request.data,
                                            partial=True,
                                        )
        serializer.is_valid(raise_exception=True)
        self.perform_update()
        
        return Response(
            {200:'Updated'},
            status=status.HTTP_200_OK,
        )
        
        
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny,])
def reset_password(request, *args, **kwargs):
    print('kwargs', kwargs)
    serializer = PasswordResetSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    return Response(
        {200: "Send an confirmation email"},
        status=status.HTTP_302_FOUND,
    )
    


    
    
    
    
    
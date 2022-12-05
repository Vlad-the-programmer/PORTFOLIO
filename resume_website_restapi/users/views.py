import json
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Auth
from django.contrib.auth import get_user_model, logout, login
from allauth.account.utils import logout_on_password_change
from django.contrib.auth.hashers import check_password
# REST FRAMEWORK 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
        raise ValueError(_("User id or token is not valid!")) 
    
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
    
    
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request):

        data = {}
        reqBody = json.loads(request.body)
        email = reqBody['email']
        print(email)
        password = reqBody['password']
        try:

            user = Profile.objects.get(email=email)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=user)[0].key
        print(token)
        if not check_password(password, user.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if user:
            if user.is_active:
                print(request.user)
                login(request, user)
                data["message"] = "user logged in"
                data["email_address"] = user.email

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
        
        
@api_view(["GET"])
def logout_user(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')
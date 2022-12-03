from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# REST_FRAMEWORK
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from dj_rest_auth.registration.serializers import RegisterSerializer
from base_utils import emails_handler
from .models import Gender

Profile = get_user_model()


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=100,
        required=False,
    )
    last_name = serializers.CharField(
        max_length=100,
        required=False,
    )
    email = serializers.EmailField(
        required=True,
    )
    gender = serializers.ChoiceField(
        choices=Gender,
        allow_blank=True,
        allow_null=True,
    )
    country = CountryField(required=False)
    featured_image = serializers.ImageField(
        allow_empty_file=True,
        required=False
    )
    username = serializers.CharField(
        max_length=100,
        required=False,
    )
    is_stuff = serializers.BooleanField(
        default=False,
        allow_null=True,
    )
    is_active = serializers.BooleanField(
        default=False,
        allow_null=True,
    )
    
    
    def get_cleaned_data(self):
        return {
            'username':       self.validated_data.get('username', ''),
            'email':          self.validated_data.get('email', ''),
            'first_name':     self.validated_data.get('first_name', ''),
            'last_name':      self.validated_data.get('last_name', ''),
            'country':        self.validated_data.get('country', ''),
            'gender':         self.validated_data.get('gender', ''),
            'featured_image': self.validated_data.get('featured_image', ''),
            'username':       self.validated_data.get('username', ''),
            'is_stuff':       self.validated_data.get('is_stuff', ''),
            'is_active':      self.validated_data.get('is_active', ''),
            
        }
    
    
class UserRegisterSerializer(serializers.ModelSerializer):
    country = CountryField(required=False, )
    password2 = serializers.CharField(
        max_length=100,
        allow_blank=True,
        allow_null=True,
        required=False,
        write_only=True,
    )
    class Meta:
        model = Profile
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'gender',
            'country',
            'featured_img',
            'password',
            'password2',
            
        )
        

    def create(self, validated_data):
        print('Create val_data', validated_data)
        validated_data.pop('password2')
        print('Create val_data2', validated_data)
        
        user = Profile.objects.create_user(**validated_data)
        
        if user:
            mail_subject = 'Please activate your account!'
            emails_handler.send_verification_email(
                self.context.get('request', None),
                user,
                template_email='account_verification_email.html',
                mail_subject = mail_subject,
            ) 
        
        return user
    
    
    def validate(self, attrs):
        if attrs.get('password', '') != attrs.get('password2', ''):
            raise ValueError(_("The two Passwords must be equal!"))
        
        return attrs
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        print(email, attrs)
        user = Profile.objects.get(email=email)
        
        if not user:
            raise Profile.DoesNotExist
        
        if user:
            mail_subject = 'Please confirm the password reset action by \
                            clicking on the link!'
            emails_handler.send_verification_email(
                self.context.get('request', None),
                user,
                template_email='reset_password_email.html',
                mail_subject = mail_subject,
            ) 
        
        return attrs
    
    
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=100,
        allow_blank=True,
        allow_null=True,
        required=False,
        write_only=True,
    )
    class Meta:
        model = Profile
        fields = (
            'password',
            'password2',
        )
        
    
    def update(self, instance, validated_data):
        print('Val data', validated_data)
        password = validated_data.get('password', '')
        
        instance.set_password(password)
        instance.save()
        
        return instance
    
    
    def validate(self, attrs):
        if attrs.get('password', '') != attrs.get('password2', ''):
            raise ValueError(_("The two Passwords must be equal!"))
        
        return attrs
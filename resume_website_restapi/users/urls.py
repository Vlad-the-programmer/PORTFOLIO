from django.urls import path
from dj_rest_auth import views as dj_rest_auth_views
from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views as custom_views

app_name='users'

urlpatterns = [
    path('all-users/', custom_views.UsersListApiView.as_view(),
         name='all-users'),
    path('registration/', custom_views.UserSignUpApiView.as_view(),
         name='register'),
    path('activate/<uuid>/<token>/', custom_views.activate_account,
         name='activate'),
    path('dj-rest-auth/login/', 
         dj_rest_auth_views.LoginView.as_view(),
         name='login'),
    path('dj-rest-auth/logout/', 
         dj_rest_auth_views.LogoutView.as_view(),
         name='logout'),
    path('password/reset/', 
         custom_views.reset_password,
         name='password_reset'),
    path('dj-rest-auth/password/reset/confirm/', 
         dj_rest_auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/change/<uuid>/<token>/',
         custom_views.PasswordChangeApiView.as_view(), 
         name='password_reset_change'),
     
    path('token/', TokenObtainPairView.as_view(), 
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), 
         name='token_refresh'),
    
]
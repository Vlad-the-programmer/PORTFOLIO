from django.urls import path
from dj_rest_auth import views as dj_rest_auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views as custom_views

app_name='users'

urlpatterns = [
     # Get a list of all users
     path('all-users/', custom_views.UsersListApiView.as_view(),
          name='all-users'),
     path('is-auth/', custom_views.user_authenticated,
          name='is_auth'),
     
     # Custom register and activate account views
     path('registration/', custom_views.UserSignUpApiView.as_view(),
          name='register'),
     path('activate/<uuid>/<token>/', custom_views.activate_account,
          name='activate'),
     
     # dj-rest-auth views
     path('password/reset/', 
          custom_views.reset_password,
          name='password_reset'),
     path('password/change/<uuid>/<token>/', 
          custom_views.PasswordChangeApiView.as_view(),
          name='password_change',
     ),
     path('dj-rest-auth/login/', 
          dj_rest_auth_views.LoginView.as_view(),
          name='login'),
     path('dj-rest-auth/logout/', 
          custom_views.logout_user,
          name='logout'),

     path('token/', TokenObtainPairView.as_view(), 
          name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), 
         name='token_refresh'),
    
     # Custom views for profile detail update delete views
     path('profile/<uuid:pk>/', 
         custom_views.ProfileDetailUpdateDeleteApiView.as_view(), 
         name='profile-detail'),
    
    
]
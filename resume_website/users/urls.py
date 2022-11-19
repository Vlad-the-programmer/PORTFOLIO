from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/detail/<int:pk>/', views.ProfileDetail.as_view(),
                                                        name='profile-detail'),
    path('profile/delete/<int:pk>/', views.ProfileDelete.as_view(),
                                                        name='profile-delete'),
    path('profile/update/<int:pk>/', views.ProfileUpdate.as_view(),
                                                        name='profile-update'),
    
    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('reset-password-validate/<int:pk>', views.reset_password_validate, name='reset-password-validate'),
    path('reset-password/<int:pk>', views.resetPassword, name='resetPassword'),
    
]
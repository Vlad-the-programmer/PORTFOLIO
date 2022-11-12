from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/detail/<int:pk>/', views.ProfileDetail.as_view(),
                                                        name='profile-detail'),
    path('profile/delete/<int:pk>/', views.ProfileDelete.as_view(),
                                                        name='profile-delete'),
    path('profile/update/<int:pk>/', views.ProfileUpdate.as_view(),
                                                        name='profile-update'),
    
]
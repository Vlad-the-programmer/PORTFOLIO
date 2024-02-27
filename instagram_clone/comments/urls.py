from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comment/create/',          views.CommentCreateView.as_view(), 
                                                        name='comment-create'),
    path('comment/update/<uuid:pk>/', views.CommentUpdateView.as_view(), 
                                                        name='comment-update'),
    path('comment/delete/<uuid:pk>/', views.CommentDeleteView.as_view(), 
                                                        name='comment-delete'),
    
    
]

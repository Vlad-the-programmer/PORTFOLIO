from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comment/create/',          views.CommentCreateView.as_view(), 
                                                        name='comment-create'),
    path('comment/update/<int:pk>/', views.CommentUpdateView.as_view(), 
                                                        name='comment-update'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), 
                                                        name='comment-delete'),
    
    
]

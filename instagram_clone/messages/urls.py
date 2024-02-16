from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    # path('messages/<slug:chat_slug',  views.CommentCreate.as_view(), 
    #                                                 name='chat-messages'),
    path('messages/create/',          views.CommentCreate.as_view(),    
                                                    name='messages-create'),
    path('messages/update/<uuid:pk>/', views.CommentUpdate.as_view(), 
                                                    name='messages-update'),
    path('messages/delete/<uuid:pk>/', views.CommentDelete.as_view(),
                                                    name='messages-delete'),
    path('chats/<uuid:user_id>/',         views.CommentDelete.as_view(),
                                                    name='user-chats'),
    path('chat/<slug:chat_slug>/detail',    views.CommentDelete.as_view(),
                                                    name='chat-detail'),
    path('chats/delete/<uuid:pk>/',    views.CommentDelete.as_view(),
                                                    name='chats-delete'),
    path('chat/create/',          views.CommentCreate.as_view(),    
                                                    name='chat-create'),
]

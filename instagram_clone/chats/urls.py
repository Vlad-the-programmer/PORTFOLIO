from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('chat/messages/create/',          views.MessageCreateView.as_view(),    
                                                    name='messages-create'),
    path('chat/messages/update/<uuid:pk>/', views.MessageUpdateView.as_view(), 
                                                    name='messages-update'),
    path('chat/messages/delete/<uuid:pk>/', views.MessageDeleteView.as_view(),
                                                    name='messages-delete'),
    path('chats/<uuid:user_id>/',       views.ChatListView.as_view(),
                                                    name='user-chats'),
    path('chat/<slug:chat_slug>/detail',    views.ChatDetailView.as_view(),
                                                    name='chat-detail'),
    path('chats/delete/<slug:chat_slug>/',  views.ChatDeleteView.as_view(),
                                                    name='chat-delete'),
    path('chat/create/<uuid:chat_to_user_id>',   views.CreateChatView.as_view(),    
                                                    name='chat-create'),
]

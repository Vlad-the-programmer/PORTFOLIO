from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('like/create/<slug:post_slug>', views.LikeCreateDeleteView.as_view(),    
                                                    name='like-create-delete'),
]

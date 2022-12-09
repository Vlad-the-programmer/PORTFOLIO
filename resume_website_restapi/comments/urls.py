from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('', 
         views.CommentListCreateApiView.as_view(),
         name='comment-list-create'),
    path('comment/<slug:slug>/', 
         views.CommentUpdateRetrieveApiView.as_view(), 
         name='comment-update-retrieve-delete'),
]

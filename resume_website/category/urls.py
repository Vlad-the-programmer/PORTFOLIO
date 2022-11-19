from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('<slug:category_slug>/', views.CategoryPostsList.as_view(),
         name='category-posts'),
    
]

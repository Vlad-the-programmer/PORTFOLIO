from django.utils.decorators import method_decorator
# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions
# Generic Api Views
from rest_framework.generics import (
                                ListCreateAPIView,
                                RetrieveUpdateDestroyAPIView
                            )

from .models import Post
from .serializers import PostListCreateSerializer


class ListCreatePostApiView(ListCreateAPIView):
    serializer_class = PostListCreateSerializer
    
    
    def get_queryset(self):
        queryset = Post.objects.filter(active=True)
        return queryset
    
    @permission_classes([permissions.IsAdminUser])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        
        return Response(
            data={'Ok': 201}, 
            status=status.HTTP_201_CREATED
            )
        

@method_decorator(permission_classes([permissions.IsAdminUser]), name='dispatch')
class PostRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostListCreateSerializer
    lookup_field = 'slug'
    
    
    def get_object(self):
        _slug = self.kwargs.get('slug')
        try:
            post = Post.objects.filter(active=True).get(slug=_slug)
        except Post.DoesNotExist:
            post = None
            
        return post
            
    
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        
        return Response(
            data={'Ok': 201}, 
            status=status.HTTP_200_OK
            )
        
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'status': 'Deleted!'}, status=status.HTTP_200_OK)
    
   
        




# REST FRAMEWORK
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategoryCRUDSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategoryCRUDSerializer
    
    
    def get_object(self):
        _slug = self.kwargs.get('slug', '')
        try:
            category = Category.objects.get(slug=_slug)
        except Category.DoesNotExist:
            category = None
            
        return category
    
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "Deleted successfully!"},
            status=status.HTTP_200_OK,
        )
        
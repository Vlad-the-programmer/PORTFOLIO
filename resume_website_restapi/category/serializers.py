from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=100,
        allow_blank=True,
        allow_null=True,
    )
    slug = serializers.SlugField(
        max_length=100,
        allow_blank=True,
    )
    
    
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'title',
            'slug'
        )
from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'title', 'url', 'description', 'created_at']
        read_only_fields = ['user', 'created_at']

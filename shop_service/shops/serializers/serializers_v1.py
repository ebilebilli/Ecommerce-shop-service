from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models import *


__all__ = [
    'ShopSerializer',
    'ShopMediaSerializer',
    'ShopBranchSerializer',
    'ShopSocialMediaSerializer',
    'ShopCommentSerializer'
]

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ShopBranchSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(read_only=True)
    slug = serializers.PrimaryKeyRelatedField(read_only=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    
    class Meta:
        model = ShopBranch
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['shop'] = self.context.get('shop')
        return super().create(validated_data)


class ShopCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    shop = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = ShopComment
        fields = '__all__'

    def validate(self, data):
        if not data.get('text') and not data.get('rating'):
            raise serializers.ValidationError('Comment text or rating must be provided.')
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['shop'] = self.context.get('shop')
        return super().create(validated_data)


class ShopMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ShopMedia
        fields = '__all__'
    
    def validate_shop(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError('You do not own this shop.')
        return value
    
    def validate_image(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise ValidationError("Image size should not exceed 5 MB.")

        valid_formats = ['image/jpeg', 'image/png']
        if value.content_type not in valid_formats:
            raise ValidationError("Unsupported image format. Use JPEG or PNG.")
        
        return value
    
    def create(self, validated_data):
        validated_data['shop'] = self.context.get('shop')
        return super().create(validated_data)


class ShopSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSocialMedia
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['shop'] = self.context.get('shop')
        return super().create(validated_data)

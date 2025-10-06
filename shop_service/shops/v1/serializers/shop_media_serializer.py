from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models.shop_media_model import ShopMedia


class ShopMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ShopMedia
        fields = '__all__'
    
    def validate_image(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise ValidationError("Image size should not exceed 5 MB.")

        valid_formats = ['image/jpeg', 'image/png']
        if value.content_type not in valid_formats:
            raise ValidationError("Unsupported image format. Use JPEG or PNG.")
        
        return value
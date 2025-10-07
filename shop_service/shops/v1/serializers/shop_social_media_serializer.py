from rest_framework import serializers

from ..models.shop_social_media_model import ShopSocialMedia


class ShopSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSocialMedia
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['shop'] = self.context.get('shop')
        return super().create(validated_data)
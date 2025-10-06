from rest_framework import serializers

from ..models.shop_social_media_model import ShopSocialMedia


class ShopSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSocialMedia
        fields = '__all__'
    
    def validate_shop(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError('You do not own this shop.')
        return value
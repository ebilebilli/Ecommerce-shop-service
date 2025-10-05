from rest_framework import serializers

from v1.models.shop_social_media_model import ShopSocialMedia


class ShopSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSocialMedia
        fields = '__all__'
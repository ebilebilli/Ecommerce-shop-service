from rest_framework import serializers

from v1.models.shop_media_model import ShopMedia


class ShopMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ShopMedia
        fields = '__all__'
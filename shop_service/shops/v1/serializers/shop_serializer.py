from rest_framework import serializers

from v1.models.shop_model import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


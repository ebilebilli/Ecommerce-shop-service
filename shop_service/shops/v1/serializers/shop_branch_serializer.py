from rest_framework import serializers

from ..models.shop_branch_model import ShopBranch


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
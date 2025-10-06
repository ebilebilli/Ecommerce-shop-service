from rest_framework import serializers

from ..models.shop_branch_model import ShopBranch


class ShopBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBranch
        fields = '__all__'
    
    def validate_shop(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError('You do not own this shop.')
        return value
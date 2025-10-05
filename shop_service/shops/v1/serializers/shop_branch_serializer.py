from rest_framework import serializers

from v1.models.shop_branch_model import ShopBranch


class ShopBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBranch
        fields = '__all__'
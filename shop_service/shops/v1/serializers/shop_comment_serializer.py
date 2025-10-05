from rest_framework import serializers

from ..models.shop_comment_model import ShopComment

class ShopCommentSerializer(serializers.ModelSerializer):
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
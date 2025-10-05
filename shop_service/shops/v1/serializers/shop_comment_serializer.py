from rest_framework import serializers

from v1.models.shop_comment_model import ShopComment

class ShopCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopComment
        fields = '__all__'

    def validate(self, data):
        if not data.get('text') and not data.get('rating'):
            raise serializers.ValidationError('Comment text or rating must be provided.')
        return data
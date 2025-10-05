from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models.shop_model import Shop
from ..models.shop_comment_model import ShopComment
from ..serializers.shop_comment_serializer import ShopCommentSerializer
from utils.pagination import CustomPagination


__all__ = [
    'CommentListByShopAPIView'
]

class CommentListByShopAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    http_method_names = ['get']

    def get(self, request, slug):
        pagination = self.pagination_class()
        shop = get_object_or_404(Shop.objects.filter(is_active=True), slug=slug)
        comments = ShopComment.objects.filter(shop=shop)
        paginator = pagination.paginate_queryset(comments, request)
        serializer = ShopCommentSerializer(paginator, many=True)

        return pagination.get_paginated_response(serializer.data)

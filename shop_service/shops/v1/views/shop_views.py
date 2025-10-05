import hashlib
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from models.shop_model import Shop
from serializers.shop_serializer import ShopSerializer
from utils.pagination import CustomPagination


class ShopListAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names =['get']
    pagination_class = CustomPagination

    def get(self, request):
        pagination = self.pagination_class()
        shops = Shop.objects.filter(is_active=True)
        paginated_shops = pagination.paginate_queryset(shops, request)
        if paginated_shops:
            serializer = ShopSerializer(paginated_shops, many=True)
            return pagination.get_paginated_response(serializer.data)
        
        return Response({'error': 'Shops not found'}, status=status.HTTP_404_NOT_FOUND)


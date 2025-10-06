from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from ..models import Shop
from ..serializers import ShopSerializer
from utils.pagination import CustomPagination


__all__ = [
    'ShopListAPIView',
    'ShopDetailAPIView',
    'CreateShopAPIView',
    'ShopManagementAPIView'
]

class ShopListAPIView(APIView):
    """List all active shops with pagination."""
    permission_classes = [AllowAny]
    http_method_names =['get']
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Get a paginated list of all active shops.",
        responses={
            200: openapi.Response(
                description="Paginated list of active shops",
                schema=ShopSerializer(many=True)
            ),
            404: "Shops not found"
        }
    )
    def get(self, request):
        pagination = self.pagination_class()
        shops = Shop.objects.filter(is_active=True)
        paginated_shops = pagination.paginate_queryset(shops, request)
        if paginated_shops:
            serializer = ShopSerializer(paginated_shops, many=True)
            return pagination.get_paginated_response(serializer.data)
        
        return Response({'error': 'Shops not found'}, status=status.HTTP_404_NOT_FOUND)


class ShopDetailAPIView(APIView):
    """Retrieve details of a specific shop by slug."""
    permission_classes = [AllowAny]
    http_method_names =['get']
   
    def get(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateShopAPIView(APIView):
    """Create a new shop. Only authenticated users can create."""
    permission_classes = [IsAuthenticated]
    http_method_names =['post']

    def post(self, request):
        user = request.user
        data = request.data
        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopManagementAPIView(APIView):
    """Update or soft-delete a shop. Only the owner can modify or delete."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']

    def patch(self, request, shop_slug):
        data = request.data
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        if shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShopSerializer(shop, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        if shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        shop.is_active = False
        shop.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
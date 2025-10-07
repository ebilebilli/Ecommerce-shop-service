from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models.shop_model import Shop
from ..models.shop_media_model import ShopMedia
from ..serializers.shop_media_serializer import ShopMediaSerializer


__all__ = [
    'ShopMediaByShopAPIView',
    'CreateShopMediaAPIView',
    'DeleteShopMediaAPIView'
]

class ShopMediaByShopAPIView(APIView):
    """Returns a media for a given shop."""
    permission_classes = [AllowAny]
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description="Get all media items for a specific shop.",
        responses={
            200: openapi.Response(
                description="List of media items",
                schema=ShopMediaSerializer(many=True)
            ),
            400: "No media found for this shop",
            404: "Shop not found"
        }
    )
    def get(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        social_medias = ShopMedia.objects.filter(shop=shop)
        if social_medias.exists():
            serializer = ShopMediaSerializer(social_medias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'No media found for this shop.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class CreateShopMediaAPIView(APIView):
    """Allows an authenticated user to create a new shop media."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Create a new media item for a shop (authenticated users only).",
        request_body=ShopMediaSerializer,
        responses={
            201: openapi.Response(
                description="Media item successfully created",
                schema=ShopMediaSerializer()
            ),
            400: "Invalid data or validation error"
        }
    )
    def post(self, request, shop_slug):
        data = request.data
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        serializer = ShopMediaSerializer(
            data=data, context={
            'request': request,
            'shop': shop
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteShopMediaAPIView(APIView):
    """Allows the owner to delete their shop media."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']
    
    @swagger_auto_schema(
        operation_description="Delete a specific shop media (only the shop owner can perform this).",
        responses={
            204: "Media successfully deleted",
            403: "Permission denied",
            404: "Media not found"
        }
    )
    def delete(self, request, media_id):
        shop_media = get_object_or_404(ShopMedia, id=media_id)
        if shop_media.shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        shop_media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
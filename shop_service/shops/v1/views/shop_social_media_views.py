from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models.shop_model import Shop
from ..models.shop_social_media_model import ShopSocialMedia
from ..serializers.shop_social_media_serializer import ShopSocialMediaSerializer


__all__ = [
    'ShopSocialMediaListByShopAPIView',
    'ShopSocialMediaDetailAPIView',
    'CreateShopSocialMediaAPIView',
    'ShopSocialMediaManagementAPIView'
]

class ShopSocialMediaListByShopAPIView(APIView):
    """Returns a list of branches for a given shop."""
    permission_classes = [AllowAny]
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description="Get all social media accounts for a given shop by slug.",
        responses={
            200: openapi.Response(
                description="List of social media accounts",
                schema=ShopSocialMediaSerializer(many=True)
            ),
            400: "No social media found for this shop",
            404: "Shop not found"
        }
    )
    def get(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        social_medias = ShopSocialMedia.objects.filter(shop=shop)
        if social_medias.exists():
            serializer = ShopSocialMediaSerializer(social_medias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'No social media found for this shop.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopSocialMediaDetailAPIView(APIView):
    """Returns detailed information about a specific social media by its id."""
    permission_classes = [AllowAny]
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_description="Get detailed info about a specific shop social media by ID.",
        responses={
            200: openapi.Response(
                description="Detailed social media info",
                schema=ShopSocialMediaSerializer()
            ),
            404: "Social media not found"
        }
    )

    def get(self, request, social_media_id):
        social_media = get_object_or_404(ShopSocialMedia, id=social_media_id)
        serializer = ShopSocialMediaSerializer(social_media)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateShopSocialMediaAPIView(APIView):
    """Allows an authenticated user to create a new shop social media."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Create a new shop social media entry.",
        request_body=ShopSocialMediaSerializer,
        responses={
            201: openapi.Response(
                description="Successfully created",
                schema=ShopSocialMediaSerializer()
            ),
            400: "Validation error"
        }
    )
    def post(self, request, shop_slug):
        data = request.data
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        serializer = ShopSocialMediaSerializer(
            data=data, context={
                'request': request,
                'shop': shop
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopSocialMediaManagementAPIView(APIView):
    """Allows the owner to update or delete their shop social media."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']

    
    @swagger_auto_schema(
        operation_description="Update a shop social media (only owner).",
        request_body=ShopSocialMediaSerializer,
        responses={
            200: openapi.Response(
                description="Updated social media",
                schema=ShopSocialMediaSerializer()
            ),
            403: "You do not have permission",
            400: "Validation error",
            404: "Social media not found"
        }
    )
    def patch(self, request, social_media_id):
        data = request.data
        social_media = get_object_or_404(ShopSocialMedia, id=social_media_id)
        if social_media.shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShopSocialMediaSerializer(social_media, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_description="Delete a shop social media (only owner).",
        responses={
            204: "Successfully deleted",
            403: "You do not have permission",
            404: "Social media not found"
        }
    )
    def delete(self, request, social_media_id):
        social_media = get_object_or_404(ShopSocialMedia, id=social_media_id)
        if social_media.shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        social_media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
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
    'CreateShopMediaAPIView'
]

class ShopMediaByShopAPIView(APIView):
    """Returns a media for a given shop."""
    permission_classes = [AllowAny]
    http_method_names = ['get']

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


class CreateMediaAPIView(APIView):
    """Allows an authenticated user to create a new shop media."""
    permission_classes = [IsAuthenticated]
    http_method_names =['post']

    def post(self, request):
        data = request.data
        serializer = ShopMediaSerializer(
            data=data, 
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

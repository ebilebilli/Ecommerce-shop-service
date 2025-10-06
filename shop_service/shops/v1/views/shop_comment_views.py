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
    'CommentListByShopAPIView',
    'CreateShopCommentAPIView',
    'CommentManagementAPIView'
]

class CommentListByShopAPIView(APIView):
    """List comments of a shop."""
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


class CreateShopCommentAPIView(APIView):
    """Create a shop comment."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, slug):
        data = request.data
        shop = get_object_or_404(Shop, slug=slug, is_active=True)
        serializer = ShopCommentSerializer(data=data, context={
            'request': request,
            'shop': shop,
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentManagementAPIView(APIView):
    """Update or delete a comment."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete', 'patch']

    def patch(self, request, comment_id):
        data = request.data
        comment = get_object_or_404(ShopComment, id=comment_id)
        if comment.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShopCommentSerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, comment_id):
        comment = get_object_or_404(ShopComment, id=comment_id)
        if comment.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.is_active = False
        comment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
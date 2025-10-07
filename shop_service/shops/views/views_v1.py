from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import * 
from ..serializers import *
from utils.pagination import CustomPagination


__all__ = [
    'ShopListAPIView',
    'ShopDetailAPIView',
    'CreateShopAPIView',
    'ShopManagementAPIView',
    'ShopBranchListByShopAPIView',
    'ShopBranchDetailAPIView',
    'CreateShopBranchAPIView',
    'ShopBranchManagementAPIView',
    'CommentListByShopAPIView',
    'CreateShopCommentAPIView',
    'CommentManagementAPIView',
    'ShopMediaByShopAPIView',
    'CreateShopMediaAPIView',
    'DeleteShopMediaAPIView',
    'ShopSocialMediaListByShopAPIView',
    'ShopSocialMediaDetailAPIView',
    'CreateShopSocialMediaAPIView',
    'ShopSocialMediaManagementAPIView'
]

# Shop Views
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

    @swagger_auto_schema(
        operation_summary="Get shop details by slug",
        responses={200: ShopSerializer()}
    )
    def get(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateShopAPIView(APIView):
    """Create a new shop. Only authenticated users can create."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_summary="Create a new shop",
        operation_description="Authenticated users can create a new shop. The current user is assigned automatically.",
        request_body=ShopSerializer,
        responses={
            201: ShopSerializer,
            400: "Validation errors"
        }
    )
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
        

# ShopBranch Views    
class ShopBranchListByShopAPIView(APIView):
    """Returns a list of active branches for a given shop."""
    permission_classes = [AllowAny]
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description="Get all active branches for a specific shop.",
        responses={
            200: openapi.Response(
                description="List of active branches",
                schema=ShopBranchSerializer(many=True)
            ),
            400: "No active branches found",
            404: "Shop not found"
        }
    )
    def get(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        shop_branches = ShopBranch.objects.filter(shop=shop, is_active=True)
        if shop_branches.exists():
            serializer = ShopBranchSerializer(shop_branches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'No active branches found for this shop.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopBranchDetailAPIView(APIView):
    """Returns detailed information about a specific branch by its slug."""
    permission_classes = [AllowAny]
    http_method_names =['get']

    @swagger_auto_schema(
        operation_description="Get detailed information about a specific shop branch by its slug.",
        responses={
            200: openapi.Response(
                description="Branch details",
                schema=ShopBranchSerializer()
            ),
            404: "Branch not found"
        }
    )
    def get(self, request, shop_branch_slug):
        shop_branch = get_object_or_404(ShopBranch, slug=shop_branch_slug, is_active=True)
        serializer = ShopBranchSerializer(shop_branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateShopBranchAPIView(APIView):
    """Allows an authenticated user to create a new shop branch."""
    permission_classes = [IsAuthenticated]
    http_method_names =['post']

    @swagger_auto_schema(
        operation_description="Create a new shop branch (authenticated users only).",
        request_body=ShopBranchSerializer,
        responses={
            201: openapi.Response(
                description="Branch successfully created",
                schema=ShopBranchSerializer()
            ),
            400: "Invalid data or validation error"
        }
    )
    def post(self, request, shop_slug):
        data = request.data
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        serializer = ShopBranchSerializer(
            data=data, context={
                'request': request,
                'shop': shop
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopBranchManagementAPIView(APIView):
    """Allows the owner to update or soft-delete their shop branch."""
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']

    @swagger_auto_schema(
        operation_description="Partially update your own shop branch.",
        request_body=ShopBranchSerializer,
        responses={
            200: openapi.Response(
                description="Branch successfully updated",
                schema=ShopBranchSerializer()
            ),
            400: "Validation error",
            403: "Permission denied",
            404: "Branch not found"
        }
    )
    def patch(self, request, shop_branch_slug):
        data = request.data
        shop_branch = get_object_or_404(ShopBranch, slug=shop_branch_slug, is_active=True)
        if shop_branch.shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShopBranchSerializer(shop_branch, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_description="Soft delete your own shop branch (sets is_active=False).",
        responses={
            204: "Branch successfully deleted",
            403: "Permission denied",
            404: "Branch not found"
        }
    )
    def delete(self, request, shop_branch_slug):
        shop_branch = get_object_or_404(ShopBranch, slug=shop_branch_slug, is_active=True)
        if shop_branch.shop.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        shop_branch.is_active = False
        shop_branch.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ShopComment Views
class CommentListByShopAPIView(APIView):
    """List comments of a shop."""
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description="Get a paginated list of comments for a specific active shop.",
        responses={
            200: openapi.Response(
                description="Paginated list of shop comments",
                schema=ShopCommentSerializer(many=True)
            ),
            404: "Shop not found"
        }
    )
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

    @swagger_auto_schema(
        operation_summary="Create a comment for a shop",
        operation_description="Authenticated users can create a comment for a given shop. The shop is determined by the slug in the URL.",
        request_body=ShopCommentSerializer,
        responses={
            201: ShopCommentSerializer,
            400: "Validation errors"
        }
    )
    def post(self, request, shop_slug):
        data = request.data
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
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

    @swagger_auto_schema(
        operation_description="Partially update a comment owned by the authenticated user.",
        request_body=ShopCommentSerializer,
        responses={
            200: openapi.Response(
                description="Successfully updated comment",
                schema=ShopCommentSerializer()
            ),
            400: "Validation error",
            403: "Permission denied",
            404: "Comment not found"
        }
    )    
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
    
    
    @swagger_auto_schema(
        operation_description="Soft delete a comment owned by the authenticated user (sets is_active=False).",
        responses={
            204: "Comment successfully deleted",
            403: "Permission denied",
            404: "Comment not found"
        }
    )
    def delete(self, request, comment_id):
        comment = get_object_or_404(ShopComment, id=comment_id)
        if comment.user != request.user:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.is_active = False
        comment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ShopMedia Views
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


# ShopScoialMedia Views
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
        
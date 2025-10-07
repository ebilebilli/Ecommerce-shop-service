from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models.shop_model import Shop
from ..models.shop_branch_model import ShopBranch
from ..serializers.shop_branch_serializer import ShopBranchSerializer


__all__ = [
    'ShopBranchListByShopAPIView',
    'ShopBranchDetailAPIView',
    'CreateShopBranchAPIView',
    'ShopBranchManagementAPIView'
]

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
        
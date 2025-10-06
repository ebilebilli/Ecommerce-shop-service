from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models.shop_model import Shop
from ..models.shop_branch_model import ShopBranch
from ..serializers.shop_branch_serializer import ShopBranchSerializer
from utils.pagination import CustomPagination


class ShopBranchListByShopAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, shop_slug):
        shop = get_object_or_404(Shop, slug=shop_slug, is_active=True)
        shop_branchs = ShopBranch.objects.filter(shop=shop, is_active=True)
        if shop_branchs.exists():
            serializer = ShopBranchSerializer(shop_branchs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'No active branches found for this shop.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopBranchDetailAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names =['get']
   
    def get(self, request, shop_branch_slug):
        shop_branch = get_object_or_404(ShopBranch, slug=shop_branch_slug, is_active=True)
        serializer = ShopBranchSerializer(shop_branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateShopBranchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names =['post']

    def post(self, request):
        user = request.user
        data = request.data
        serializer = ShopBranchSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopBranchManagementAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']

    def patch(self, request, shop_id):
        data = request.data
        shop_branch = get_object_or_404(ShopBranch, id=shop_id, is_active=True)
        if shop_branch.user.id != request.user.id:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShopBranchSerializer(shop_branch, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, shop_id):
        shop_branch = get_object_or_404(ShopBranch, id=shop_id, is_active=True)
        if shop_branch.user.id != request.user.id:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        shop_branch.is_active = False
        shop_branch.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
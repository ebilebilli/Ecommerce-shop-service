from django.urls import path
from .views import *


urlpatterns = [
    path(
        'shops/', 
        ShopListAPIView.as_view(),
        name='shop-list'
    ),         
    path(
        'shops/<slug:shop_slug>/', 
        ShopDetailAPIView.as_view(), 
        name='shop-detail'
    ),  
    path(
        'shops/create/',
        CreateShopAPIView.as_view(), 
        name='shop-create'
    ),
    path(
        'shops/management/',
        ShopManagementAPIView.as_view(), 
        name='shop-manage'
    ),
    path(
        'shops/<slug:shop_slug>/comments/', 
        CommentListByShopAPIView.as_view(),
        name='comment-list'
    ),
    path(
        'shops/<slug:shop_slug>/create/', 
        CreateShopCommentAPIView.as_view(),
        name='create-shop-comment'
    ),
    path(
        'comments/<int:comment_id>/management/',
        CommentManagementAPIView.as_view(), 
        name='comment-manage'
    ),            
]
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
]
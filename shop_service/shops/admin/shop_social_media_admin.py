from django.contrib import admin

from shops.v1.models.shop_social_media_model import ShopSocialMedia


@admin.register(ShopSocialMedia)
class ShopSocialMediaAdmin(admin.ModelAdmin):
    list_display = ('shop', 'media_name', 'media_url')
    search_fields = ('shop__name', 'media_name')
    list_filter = ('media_name',)

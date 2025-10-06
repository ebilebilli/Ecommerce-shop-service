from django.contrib import admin
from django.utils.html import format_html

from shops.v1.models.shop_media_model import ShopMedia


@admin.register(ShopMedia)
class ShopMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'image_preview', 'alt_text')
    search_fields = ('shop__name', 'alt_text')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

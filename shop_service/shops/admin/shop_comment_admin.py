from django.contrib import admin

from shops.v1.models.shop_comment_model import ShopComment


@admin.register(ShopComment)
class ShopCommentAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'shop', 'text', 'rating', 'created_at', 'updated_at', 'is_active')
    list_filter = ('rating',)
    search_fields = ('text', 'shop__name')
    readonly_fields = ('created_at', 'updated_at')

    def user_display(self, obj):
        return obj.user.username if obj.user else f"User ID: {obj.user_id}"
    user_display.short_description = 'User'

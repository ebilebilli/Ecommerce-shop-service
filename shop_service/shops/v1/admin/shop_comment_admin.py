from django.contrib import admin

from models.shop_comment_model import ShopComment


@admin.register(ShopComment)
class ShopCommentAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'shop', 'text', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating',)
    search_fields = ('text', 'shop__name')
    readonly_fields = ('created_at', 'updated_at')

    def user_display(self, obj):
        # Hazırda User modeli var, gələcəkdə isə user_id göstərə bilərik
        return obj.user.username if obj.user else f"User ID: {obj.user_id}"
    user_display.short_description = 'User'

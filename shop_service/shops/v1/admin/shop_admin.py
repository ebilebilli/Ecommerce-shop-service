from django.contrib import admin

from models.shop_model import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_verified', 'is_active')
    search_fields = ('name', 'slug')
    readonly_fields = ('created_at', 'updated_at')

from django.contrib import admin

from shops.v1.models.shop_branch_model import ShopBranch


@admin.register(ShopBranch)
class ShopBranchAdmin(admin.ModelAdmin):
    list_display = ('shop', 'shop_branch_name', 'phone_number', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('shop_branch_name', 'shop__name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

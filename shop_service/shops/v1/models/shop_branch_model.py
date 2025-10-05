from django.db import models

from .shop_model import Shop


class ShopBranch(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )
    about = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name='About shop branch'
    )
    phone_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Shop branch phone number'
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='longitude'   
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active'
    )

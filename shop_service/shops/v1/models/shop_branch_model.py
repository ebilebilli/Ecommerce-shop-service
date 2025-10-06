from django.db import models

from .shop_model import Shop
from utils.validators import not_only_whitespace


class ShopBranch(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        verbose_name='Shop'
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Shop branch slug'
    )
    shop_branch_name = models.CharField(
        max_length=100,
        validators=[not_only_whitespace],
        verbose_name='Shop branch name'
    )
    about = models.TextField(
        max_length=2000,
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

    def __str__(self):
        return f'{self.shop.id}: {self.shop_branch_name}'
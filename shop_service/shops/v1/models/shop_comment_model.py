import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .shop_model import Shop
from utils.validators import not_only_whitespace


class ShopComment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='User'
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Shop'
    )
    text = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        validators=[not_only_whitespace],
        verbose_name='Comment text'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name='Comment rating(1-5)'
    )

    
    def clean(self):
        if not self.text and not self.rating:
            raise ValidationError('Comment text or rating must be provided.')

    def __str__(self):
        return f'{self.user.id} add comment to {self.shop.id}'
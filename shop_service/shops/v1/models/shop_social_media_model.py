from django.db import models

from .shop_model import Shop


class ShopSocialMedia(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )
    media_name = models.CharField(
        max_length=50,
        verbose_name='Media name'
    )
    media_url = models.URLField(
        max_length=200,
        verbose_name='Media url'
    )

    def __str__(self):
        return f'{self.shop.id}: {self.media_name}'
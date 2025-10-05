from django.db import models

from .shop_model import Shop


class ShopMedia(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        verbose_name='Shop'
    )
    image = models.ImageField(
        upload_to='shop_media',
        null=False,
        verbose_name='Images of shop'
    )
    alt_text = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name='Alt text for image'
        )

    def __str__(self):
        return self.id
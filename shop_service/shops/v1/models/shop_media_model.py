from django.db import models

from v1.models import Shop


class ShopMedia(models.Model):
    shop = models.ForeignKey(
        Shop
    )
    image = models.ImageField(
        upload_to='shop_media',
        null=False,
        verbose_name='images of shop'
    )
    alt_text = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name='alt text for image'
        )

    def __str__(self):
        return self.id
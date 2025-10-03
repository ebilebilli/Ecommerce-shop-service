import uuid
from django.db import models
from django.contrib.auth.models import User

from utils.validators import not_only_whitespace


class Shop(models.Model):
    user = models.OneToOneField(     # This connection is temporary.It will change
        User,
        related_name='shops',
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )    
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
        blank=True,
        verbose_name='shop slug'
    )
    name = models.CharField(
        max_length=100,
        validators=[not_only_whitespace],
        verbose_name='shop name'
    )
    about = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        validators=[not_only_whitespace],
        verbose_name='about shop'
    )
    profile = models.ImageField(
        upload_to='shop_profiles',
        blank=True,
        null=True,
        verbose_name='shop profile photo'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='shop verified'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='shop activity'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='shop created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='shop updated at'
    )

    def __str__(self):
        return self.name
 
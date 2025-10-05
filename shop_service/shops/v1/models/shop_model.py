import uuid
from django.db import models
from django.contrib.auth.models import User

from utils.validators import not_only_whitespace


class Shop(models.Model):
    user = models.OneToOneField(     # This connection is temporary.It will change
        User,
        related_name='shops',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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
        verbose_name='Shop slug'
    )
    name = models.CharField(
        max_length=100,
        validators=[not_only_whitespace],
        verbose_name='Shop name'
    )
    about = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        validators=[not_only_whitespace],
        verbose_name='About shop'
    )
    profile = models.ImageField(
        upload_to='shop_profiles',
        blank=True,
        null=True,
        verbose_name='Shop profile photo'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Shop verified'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Shop activity'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Shop created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Shop updated at'
    )

    def __str__(self):
        return self.name
 
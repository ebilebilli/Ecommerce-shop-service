from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import transaction

from .v1.models import Shop


@receiver(pre_save, sender=Shop)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        unique_slug = base_slug
        counter = 1
        while Shop.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{base_slug}-{counter}'
            counter += 1
        instance.slug = unique_slug
from django.db import models
from django.conf import settings

from .utils import create_shortened_url

REDIRECT_URL = f"{settings.HOST_URL}/redirect/"


class Shortener(models.Model):
    original_url = models.URLField(unique=True)
    short_url = models.CharField(max_length=6, unique=True, blank=True)
    redirect_link = models.CharField(max_length=30, unique=True, blank=True)
    last_redirect_time = models.DateTimeField(null=True)
    redirect_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    ip = models.CharField(max_length=50, blank=True)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        if not self.short_url:
            self.short_url = create_shortened_url(self)
            self.redirect_link = f"{REDIRECT_URL}{self.short_url}/"

        super().save()

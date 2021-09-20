from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    TIERS = (
        ('CUSTOM', 'custom'),
        ('BASIC', 'basic'),
        ('PREMIUM', 'premium'),
        ('ENTERPRISE', 'enterprise')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.CharField(max_length=10, choices=TIERS)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

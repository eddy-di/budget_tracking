import secrets
from django.db import models
from django.db.models.query import QuerySet
from wallet.models.wallet import Wallet
from django.contrib.auth.models import User
from django.utils import timezone


class InviteManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class Invite(models.Model):
    token = models.CharField(
        max_length=255, 
        unique=True,
        default=timezone.now()
        )
    wallet = models.ForeignKey(
        Wallet, 
        on_delete=models.CASCADE
        )
    expiration_date = models.DateTimeField(
        default=timezone.now()+timezone.timedelta(days=1)
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(
        default=False
    )
    email = models.EmailField(
        max_length=254
    )

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


    
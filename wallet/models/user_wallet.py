from django.db import models
from .wallet import Wallet
from django.contrib.auth.models import User


class UserWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class Wallet(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    user = models.ManyToManyField(User, related_name='wallet_users')

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_detail_url(self):
        return reverse('wallet:wallet_index',
                       args=[self.id,
                             self.user.id])
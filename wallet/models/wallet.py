from django.db import models
from django.utils.text import slugify 

class Wallet(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
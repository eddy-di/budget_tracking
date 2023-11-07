from django.db import models
from .category import Category


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sub_category_name
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Product (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} Product'


class Category (MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name} Category'


class Brand (models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name} Brand'

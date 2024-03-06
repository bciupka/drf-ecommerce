from django.contrib import admin
from .models import Brand, Category, Product, ProductLine, ProductImage
from django.urls import reverse
from django.utils.safestring import mark_safe


class EditLink:
    def edit(self, instance):
        url = reverse(f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
                      args=[instance.id])
        if instance.pk:
            link = mark_safe(f'<a href="{url}">edit</a>')
            return link
        else:
            return ''


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineInLine(EditLink, admin.TabularInline):
    model = ProductLine
    readonly_fields = ["edit"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInLine]


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Brand)
admin.site.register(Category)

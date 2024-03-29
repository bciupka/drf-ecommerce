from django.contrib import admin
from .models import Category, Product, ProductLine, ProductImage, Attribute, AttributeValue, ProductType
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


class AttributeValueInProductLineInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through


class AttributeValueInProductInline(admin.TabularInline):
    model = AttributeValue.product_attribute_value.through


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInLine, AttributeValueInProductInline]


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueInProductLineInline]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]


admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)

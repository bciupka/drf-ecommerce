from rest_framework import serializers
from .models import Brand, Category, Product, ProductLine, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category_name']


class BrandSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='name')

    class Meta:
        model = Brand
        fields = ['brand_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id', 'productline']


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        exclude = ['id', 'is_active', 'product']


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(source='category.name')
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'is_digital', 'brand_name', 'category_name', 'product_line']

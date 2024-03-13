from rest_framework import serializers
from .models import Category, Product, ProductLine, ProductImage, Attribute, AttributeValue
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id', 'product_line']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('name', 'id')


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        exclude = ('id',)


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_values = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        exclude = ['id', 'is_active', 'product']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av = data.pop('attribute_values')
        attr_values = {}
        for i in av:
            attr_values[i['attribute']['id']] = i['attribute_value']
        data['specifications'] = attr_values
        return data

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', required=False)
    product_line = ProductLineSerializer(many=True)
    specs = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'is_digital', 'category_name', 'product_line', 'specs']

    @extend_schema_field(AttributeSerializer)
    def get_specs(self, obj):
        specs = Attribute.objects.filter(product_type_attribute__product_from_type__id=obj.id)
        return AttributeSerializer(specs, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        specs = data.pop('specs')
        type_specification = {}
        for i in specs:
            type_specification[i['id']] = i['name']
        data['type_specification'] = type_specification
        return data

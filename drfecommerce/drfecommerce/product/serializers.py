from rest_framework import serializers
from .models import Category, Product, ProductLine, ProductImage, Attribute, AttributeValue
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category', 'slug']


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
        fields = ['price', 'sku', 'stock_qty', 'order', 'product_image', 'attribute_values']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av = data.pop('attribute_values')
        attr_values = {}
        for i in av:
            attr_values[i['attribute']['name']] = i['attribute_value']
        data['specifications'] = attr_values
        return data

class ProductSerializer(serializers.ModelSerializer):
    product_line = ProductLineSerializer(many=True)
    attribute_values = AttributeValueSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'pid',  'description', 'product_line', 'attribute_values']

    # @extend_schema_field(AttributeSerializer)
    # def get_specs(self, obj):
    #     specs = Attribute.objects.filter(product_type_attribute__product_from_type__id=obj.id)
    #     return AttributeSerializer(specs, many=True).data
    #
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     specs = data.pop('specs')
    #     type_specification = {}
    #     for i in specs:
    #         type_specification[i['id']] = i['name']
    #     data['type_specification'] = type_specification
    #     return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av = data.pop('attribute_values')
        attr_values = {}
        for i in av:
            attr_values[i['attribute']['name']] = i['attribute_value']
        data['attributes'] = attr_values
        return data


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ['price', 'product_image']

class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'pid', 'product_line', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        pl = data.pop('product_line')
        if pl:
            price = pl[0]['price']
            image = pl[0]['product_image']
            data['price'] = price
            data['image'] = image

        return data

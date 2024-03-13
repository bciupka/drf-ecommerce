import factory
from drfecommerce.product.models import (Category, Product, ProductLine, ProductImage, ProductType, Attribute,
                                         AttributeValue, ProductLineAttributeValue, ProductAttributeValue)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'test_category_{n}')
    slug = factory.Sequence(lambda n: f'test_cat_slug_{n}')


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        skip_postgeneration_save = True

    name = factory.Sequence(lambda x: f'product_type_{x}')

    @factory.post_generation
    def attributes(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attributes.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f'test_product_{n}')
    slug = factory.Sequence(lambda n: f'test_p_{n}')
    pid = factory.Sequence(lambda n: f'{n}')
    description = 'desc'
    category = factory.SubFactory(CategoryFactory)
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_values(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_values.add(*extracted)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        skip_postgeneration_save = True

    price = factory.Sequence(lambda n: float(n))
    sku = factory.Sequence(lambda n: f'sku_{n}')
    stock_qty = 10
    weight = 1.000
    product = factory.SubFactory(ProductFactory)
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_values(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_values.add(*extracted)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = factory.Sequence(lambda x: f"{x}_text")
    url = factory.Sequence(lambda x: f"somefile_{x}.jpg")
    product_line = factory.SubFactory(ProductLineFactory)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = factory.Sequence(lambda x: f'attr_{x}')
    description = 'test-decription'


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = factory.Sequence(lambda x: f'attr_val_{x}')
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLineAttributeValue

    product_line = factory.SubFactory(ProductLineFactory)
    attribute_value = factory.SubFactory(AttributeValueFactory)


class ProductAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeValue

    product = factory.SubFactory(ProductLineFactory)
    attribute_value = factory.SubFactory(AttributeValueFactory)

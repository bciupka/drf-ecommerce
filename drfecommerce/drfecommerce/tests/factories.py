import factory
from drfecommerce.product.models import (Category, Product, Brand, ProductLine, ProductImage, ProductType, Attribute,
                                         AttributeValue)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'test_category_{n}')
    slug = factory.Sequence(lambda n: f'test_cat_slug_{n}')
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f'test_brand_{n}')
    slug = factory.Sequence(lambda n: f'test_brand_slug_{n}')
    is_active = True


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

    name = 'test_product'
    slug = factory.Sequence(lambda n: f'test_p_{n}')
    description = 'desc'
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    product_type = factory.SubFactory(ProductTypeFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine
        skip_postgeneration_save = True

    price = factory.Sequence(lambda n: float(n))
    sku = factory.Sequence(lambda n: f'sku_{n}')
    stock_qty = 10
    product = factory.SubFactory(ProductFactory)
    is_active = True

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
    productline = factory.SubFactory(ProductLineFactory)


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

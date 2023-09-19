import factory
from drfecommerce.product.models import Category, Product, Brand, ProductLine


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


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = 'test_product'
    slug = factory.Sequence(lambda n: f'test_p_{n}')
    description = 'desc'
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = factory.Sequence(lambda n: float(n))
    sku = factory.Sequence(lambda n: f'sku_{n}')
    stock_qty = 10
    product = factory.SubFactory(ProductFactory)
    is_active = True

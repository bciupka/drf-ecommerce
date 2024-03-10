import pytest
from pytest_factoryboy import register
from drfecommerce.tests.factories import (CategoryFactory, BrandFactory, ProductFactory, ProductLineFactory,
                                          ProductImageFactory, ProductTypeFactory, AttributeFactory,
                                          AttributeValueFactory)
from rest_framework.test import APIClient


register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductTypeFactory)
register(AttributeFactory)
register(AttributeValueFactory)


@pytest.fixture
def api_client():
    return APIClient

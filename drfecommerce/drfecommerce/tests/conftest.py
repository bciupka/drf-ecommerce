import pytest
from pytest_factoryboy import register
from drfecommerce.tests.factories import (CategoryFactory, ProductFactory, ProductLineFactory,
                                          ProductImageFactory, ProductTypeFactory, AttributeFactory,
                                          AttributeValueFactory, ProductLineAttributeValueFactory,
                                          ProductAttributeValueFactory)
from rest_framework.test import APIClient


register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductTypeFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductLineAttributeValueFactory)
register(ProductAttributeValueFactory)


@pytest.fixture
def api_client():
    return APIClient

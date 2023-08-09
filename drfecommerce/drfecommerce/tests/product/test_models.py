import pytest


pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        post = category_factory(name='test_category')
        assert post.__str__() == 'test_category Category'


class TestProductModel:
    def test_str_method(self, brand_factory):
        post = brand_factory(name='test_brand')
        assert post.__str__() == 'test_brand Brand'


class TestBrandModel:
    def test_str_method(self, product_factory):
        post = product_factory()
        assert post.__str__() == 'test_product Product'

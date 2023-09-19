import pytest
from django.core.exceptions import ValidationError


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


class TestProductLineModel:
    def test_str_method(self, product_factory, product_line_factory):
        post = product_line_factory(sku='sku_1', product=product_factory(name='for_pl_prod'))
        assert post.__str__() == 'for_pl_prod Product Line sku_1'

    def test_clean(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()
        with pytest.raises(ValidationError):
            product_line_factory(order=0).clean()

import json
import pytest


pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:

    endpoint = '/api/category/'

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4, is_active=True)
        response = api_client().get(self.endpoint)
        # print(json.loads(response.content))
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoints:

    endpoint = '/api/product/'

    def test_get_by_slug(self, product_factory, api_client):
        product_factory(slug='test_s', is_active=True)
        product_factory(slug='test_s2', is_active=True)
        response = api_client().get(f'{self.endpoint}test_s/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_get_by_cat_slug(self, category_factory, product_factory, api_client):
        cat = category_factory(slug='c_test', is_active=True)
        product_factory(category=cat, is_active=True)
        response = api_client().get(f'{self.endpoint}category/{cat.slug}/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

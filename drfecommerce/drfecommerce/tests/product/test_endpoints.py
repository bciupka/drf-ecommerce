import json
import pytest


pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:

    endpoint = '/api/category/'

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        # print(json.loads(response.content))
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestBrandEndpoints:

    endpoint = '/api/brand/'

    def test_brand_get(self, brand_factory, api_client):
        brand_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoints:

    endpoint = '/api/product/'

    def test_get_all(self, product_factory, api_client):
        product_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_get_by_slug(self, product_factory, api_client):
        obj = product_factory(slug='test_s')
        response = api_client().get(f'{self.endpoint}{obj.slug}/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_get_by_cat_slug(self, category_factory, product_factory, api_client):
        cat = category_factory(slug='c_test')
        obj = product_factory(category=cat)
        response = api_client().get(f'{self.endpoint}category/{cat.slug}/all/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

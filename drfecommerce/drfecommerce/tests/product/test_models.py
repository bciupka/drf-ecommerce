import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from drfecommerce.product.models import Category, Product, ProductLine


pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        post = category_factory(name='test_category')
        assert post.__str__() == 'test_category Category'

    def test_name_max_length(self, category_factory):
        name = 'x' * 236
        post = category_factory(name=name)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = 'x' * 256
        post = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_name_uniqueness(self, category_factory):
        category_factory(name='test_name')
        with pytest.raises(IntegrityError):
            category_factory(name='test_name')

    def test_slug_uniqueness(self, category_factory):
        category_factory(slug='test_slug')
        with pytest.raises(IntegrityError):
            category_factory(slug='test_slug')

    def test_is_active_default(self, category_factory):
        post = category_factory()
        assert post.is_active is False

    def test_protected_on_delete(self, category_factory):
        obj_1 = category_factory()
        category_factory(parent=obj_1)
        with pytest.raises(IntegrityError):
            obj_1.delete()

    def test_parent_null_default(self, category_factory):
        post = category_factory()
        assert post.parent is None

    def test_manager_is_active(self, category_factory):
        category_factory(is_active=True)
        category_factory()
        amount = Category.objects.is_active().count()
        assert amount == 1

    def test_manager_all(self,category_factory):
        category_factory(is_active=True)
        category_factory()
        amount = Category.objects.all().count()
        assert amount == 2


class TestProductModel:
    def test_str_method(self, product_factory, attribute_value_factory):
        obj = attribute_value_factory()
        post = product_factory(name='test_product', attribute_values=(obj,))
        assert post.__str__() == 'test_product Product'

    def test_name_max_length(self, product_factory):
        name = 'x' * 236
        post = product_factory(name=name)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_slug_max_length(self, product_factory):
        slug = 'x' * 256
        post = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_pid_max_length(self, product_factory):
        pid = 'x' * 11
        post = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            post.full_clean()

    def test_name_uniqueness(self, product_factory):
        product_factory(name='test')
        with pytest.raises(IntegrityError):
            product_factory(name='test')

    def test_slug_uniqueness(self, product_factory):
        product_factory(slug='test')
        with pytest.raises(IntegrityError):
            product_factory(slug='test')

    def test_pid_uniqueness(self, product_factory):
        product_factory(pid='test')
        with pytest.raises(IntegrityError):
            product_factory(pid='test')

    def test_is_digital_default(self, product_factory):
        post = product_factory()
        assert post.is_digital is False

    def test_is_active_default(self, product_factory):
        post = product_factory()
        assert post.is_active is False

    def test_category_protected_delete(self, product_factory, category_factory):
        obj = category_factory()
        product_factory(category=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_manager_is_active(self, product_factory):
        product_factory()
        product_factory(is_active=True)
        amount = Product.objects.is_active().count()
        assert amount == 1

    def test_manager_all(self, product_factory):
        product_factory()
        product_factory(is_active=True)
        amount = Product.objects.all().count()
        assert amount == 2

    def test_product_type_delete_protect(self, product_type_factory, product_factory):
        obj = product_type_factory()
        product_factory(product_type=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_attribute_duplicate(self, attribute_factory, attribute_value_factory, product_factory,
                                 product_attribute_value_factory):
        obj_1 = attribute_factory()
        obj_2 = attribute_value_factory(attribute=obj_1)
        obj_3 = attribute_value_factory(attribute=obj_1)
        obj_4 = product_factory()
        product_attribute_value_factory(attribute_value=obj_2, product=obj_4)
        with pytest.raises(ValidationError):
            product_attribute_value_factory(attribute_value=obj_3, product=obj_4)


class TestProductLineModel:
    def test_str_method(self, product_factory, product_line_factory, attribute_value_factory):
        obj = attribute_value_factory()
        post = product_line_factory(sku='sku_1', product=product_factory(name='for_pl_prod'), attribute_values=(obj,))
        assert post.__str__() == 'for_pl_prod Product Line sku_1'

    def test_price_decimal_places(self, product_line_factory):
        with pytest.raises(ValidationError):
            product_line_factory(price=1.045)

    def test_price_max_digits(self, product_line_factory):
        with pytest.raises(ValidationError):
            product_line_factory(price=1000.04)

    def test_sku_max_length(self, product_line_factory):
        sku = 'x' * 11
        with pytest.raises(ValidationError):
            post = product_line_factory(sku=sku)
            post.full_clean()

    def test_product_is_active_default(self, product_line_factory):
        post = product_line_factory()
        assert post.is_active is False

    def test_product_delete_protect(self, product_factory, product_line_factory):
        obj = product_factory()
        product_line_factory(product=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_manager_is_active(self, product_line_factory):
        product_line_factory()
        product_line_factory(is_active=True)
        amount = ProductLine.objects.is_active().count()
        assert amount == 1

    def test_manager_all(self, product_line_factory):
        product_line_factory()
        product_line_factory(is_active=True)
        amount = ProductLine.objects.all().count()
        assert amount == 2

    def test_order_uniqueness(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_order_zero(self, product_line_factory):
        with pytest.raises(ValidationError):
            product_line_factory(order=0).clean()

    def test_product_type_delete_protect(self, product_type_factory, product_line_factory):
        obj = product_type_factory()
        product_line_factory(product_type=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_attribute_duplicate(self, attribute_factory, attribute_value_factory, product_line_factory,
                                 product_line_attribute_value_factory):
        obj_1 = attribute_factory()
        obj_2 = attribute_value_factory(attribute=obj_1)
        obj_3 = attribute_value_factory(attribute=obj_1)
        obj_4 = product_line_factory()
        product_line_attribute_value_factory(attribute_value=obj_2, product_line=obj_4)
        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(attribute_value=obj_3, product_line=obj_4)


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj = product_line_factory(sku='123')
        post = product_image_factory(product_line=obj, alternative_text='front_pic')
        assert post.__str__() == "123 image front_pic"

    def test_alternative_text_max_length(self, product_image_factory):
        alt = 'x' * 101
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alt)

    def test_order_uniqueness(self, product_image_factory, product_line_factory):
        obj = product_line_factory()
        product_image_factory(product_line=obj)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj).clean()

    def test_order_zero(self, product_image_factory):
        with pytest.raises(ValidationError):
            product_image_factory(order=0).clean()


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        obj = attribute_factory()
        post = product_type_factory(name='test_name', attributes=(obj,))
        assert post.__str__() == 'test_name'

    def test_name_max_length(self, product_type_factory):
        name = 'x' * 101
        with pytest.raises(ValidationError):
            product_type_factory(name=name).full_clean()

    def test_parent_delete_protect(self, product_type_factory):
        obj = product_type_factory()
        product_type_factory(parent=obj)
        with pytest.raises(IntegrityError):
            obj.delete()


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        post = attribute_factory(name='test_name')
        assert post.__str__() == 'test_name'

    def test_name_max_length(self, attribute_factory):
        name = 'x' * 101
        with pytest.raises(ValidationError):
            attribute_factory(name=name).full_clean()


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj = attribute_factory(name='test_attr')
        post = attribute_value_factory(attribute_value='test_val', attribute=obj)
        assert post.__str__() == 'test_attr-test_val'

    def test_attribute_value_max_length(self, attribute_value_factory):
        attribute_value = 'x' * 101
        with pytest.raises(ValidationError):
            attribute_value_factory(attribute_value=attribute_value).full_clean()

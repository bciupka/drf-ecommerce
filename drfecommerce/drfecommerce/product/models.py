from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError
from django.db.models.functions import Random


class IsActiveQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = IsActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name} Category'


class Product(models.Model):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(max_length=200, blank=True)
    is_digital = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='product_from_type')
    attribute_values = models.ManyToManyField('AttributeValue', through='ProductAttributeValue',
                                              related_name='product_attribute_value')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = IsActiveQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} Product'


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attribute_value')

    def __str__(self):
        return f"{self.attribute.name}-{self.attribute_value}"


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    attributes = models.ManyToManyField(Attribute, through='ProductTypeAttribute',
                                        related_name='product_type_attribute')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='product_type_attribute_pt')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='product_type_attribute_a')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['product_type', 'attribute'],
                                               name='product_type_attribute_uniqueness')]


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=10)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_line')
    weight = models.FloatField()
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='product_line_from_type')
    attribute_values = models.ManyToManyField(AttributeValue, through="ProductLineAttributeValue",
                                              related_name="product_line_attribute_value")
    is_active = models.BooleanField(default=False)
    order = OrderField(blank=True, unique_for_field='product')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = IsActiveQuerySet.as_manager()

    def __str__(self):
        return f'{self.product.name} Product Line {self.sku}'

    def clean(self, exclude=None):
        if self.order == 0:
            raise ValidationError('Order needs to be grater than 0')
        queryset = ProductLine.objects.filter(product=self.product)
        for instance in queryset:
            if instance.id != self.id and instance.order == self.order:
                raise ValidationError('Duplicate order number')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,
                                        related_name="product_line_attribute_value_av")
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     related_name="product_line_attribute_value_pl")

    class Meta:
        constraints = [models.UniqueConstraint(fields=('attribute_value', 'product_line'),
                                               name='product_line_attribute_value_key_uniqueness')]

    def clean(self):
        exist = ProductLineAttributeValue.objects.filter(attribute_value=self.attribute_value,
                                                         product_line=self.product_line).exists()
        # if not exist:
        #     ids = (Attribute.objects.filter(attribute_value__product_line_attribute_value=self.product_line)
        #            .values_list('pk', flat=True))
        #
        #     if self.attribute_value.attribute.id in ids:
        #         raise ValidationError("Duplicated attribute for this product line")

        if not exist:
            exist_2 = ProductLineAttributeValue.objects.filter(
                attribute_value__attribute__id=self.attribute_value.attribute.id,
                product_line=self.product_line).exists()

            if exist_2:
                raise ValidationError('Duplicated attribute for product line')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attribute_value_p')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,
                                        related_name='product_attribute_value_av')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'attribute_value'],
                                               name='product_attribute_value_uniqueness')]

    def clean(self):
        exist = (ProductAttributeValue.objects.filter(product=self.product, attribute_value=self.attribute_value)
                 .exists())
        if not exist:
            exist_2 = (ProductAttributeValue.objects.filter(product=self.product,
                                                           attribute_value__attribute=self.attribute_value.attribute).
                       exists())

            if exist_2:
                raise ValidationError('Duplicated attribute for product')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default='test.jpg')
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_for_field='product_line', blank=True)

    objects = IsActiveQuerySet.as_manager()

    def clean(self, exclude=None):
        if self.order == 0:
            raise ValidationError('Order needs to be grater than 0')
        queryset = ProductImage.objects.filter(product_line=self.product_line)
        for instance in queryset:
            if instance.id != self.id and instance.order == self.order:
                raise ValidationError('Duplicate order number')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_line.sku} image {self.alternative_text}'

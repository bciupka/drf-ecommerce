from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError


class ActiveQuerySet(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name} Category'


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=False)

    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} Brand'


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    objects = ActiveQuerySet.as_manager()

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
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_line')
    attribute_values = models.ManyToManyField(AttributeValue, through="ProductLineAttributeValue",
                                              related_name="product_line_attribute_value")
    is_active = models.BooleanField(default=False)
    order = OrderField(blank=True, unique_for_field='product')

    objects = ActiveQuerySet.as_manager()

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
                raise ValidationError('no no no')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default='test.jpg')
    productline = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_for_field='productline', blank=True)

    objects = ActiveQuerySet.as_manager()

    def clean(self, exclude=None):
        if self.order == 0:
            raise ValidationError('Order needs to be grater than 0')
        queryset = ProductImage.objects.filter(productline=self.productline)
        for instance in queryset:
            if instance.id != self.id and instance.order == self.order:
                raise ValidationError('Duplicate order number')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.alternative_text} image'

# Generated by Django 4.2.3 on 2023-09-01 08:51

from django.db import migrations
import drfecommerce.product.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_brand_is_active_category_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productline',
            name='order',
            field=drfecommerce.product.fields.OrderField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
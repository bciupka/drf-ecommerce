# Generated by Django 4.2.3 on 2024-03-09 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_producttype_producttypeattribute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productline',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.producttype'),
        ),
    ]
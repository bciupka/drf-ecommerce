# Generated by Django 4.2.3 on 2024-03-13 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_product_product_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attribute_value_av', to='product.attributevalue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attribute_value_p', to='product.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='productattributevalue',
            constraint=models.UniqueConstraint(fields=('product', 'attribute_value'), name='product_attribute_value_uniqueness'),
        ),
    ]
# Generated by Django 4.2.3 on 2024-03-04 20:06

from django.db import migrations, models
import django.db.models.deletion
import drfecommerce.product.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_brand_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative_text', models.CharField(max_length=100)),
                ('url', models.ImageField(default='test.jpg', upload_to=None)),
                ('order', drfecommerce.product.fields.OrderField(blank=True)),
                ('productline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='product.productline')),
            ],
        ),
    ]
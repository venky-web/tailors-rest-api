# Generated by Django 4.0 on 2022-01-01 14:06

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.product_image_file_path)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField()),
                ('created_by', models.CharField(max_length=255)),
                ('updated_by', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', related_query_name='product_image', to='products.product')),
            ],
        ),
    ]

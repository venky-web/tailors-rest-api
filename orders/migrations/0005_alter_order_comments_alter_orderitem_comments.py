# Generated by Django 4.0 on 2022-01-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='comments',
            field=models.TextField(blank=True, default='', max_length=512),
        ),
    ]

# Generated by Django 4.0 on 2021-12-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_deleted',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_deleted',
            field=models.CharField(default='N', max_length=1),
        ),
    ]
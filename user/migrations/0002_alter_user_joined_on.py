# Generated by Django 4.0 on 2021-12-19 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
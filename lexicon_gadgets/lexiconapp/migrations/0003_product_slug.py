# Generated by Django 4.1.2 on 2022-11-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexiconapp', '0002_remove_customer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]

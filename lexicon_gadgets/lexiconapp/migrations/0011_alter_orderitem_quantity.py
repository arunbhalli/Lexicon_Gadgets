# Generated by Django 4.1.2 on 2022-11-23 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexiconapp', '0010_alter_orderitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]

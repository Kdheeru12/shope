# Generated by Django 3.1.7 on 2021-03-17 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop1', '0005_auto_20210318_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop1.customer'),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop1.product'),
        ),
    ]

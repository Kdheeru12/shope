# Generated by Django 3.1.7 on 2021-04-04 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop1', '0007_auto_20210403_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.IntegerField(blank=True, default=0, max_length=10, null=True),
        ),
    ]

# Generated by Django 5.1.2 on 2025-05-11 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManasVerse', '0006_remove_orderitem_price_remove_orderitem_product_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

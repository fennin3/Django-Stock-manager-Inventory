# Generated by Django 3.1.1 on 2020-09-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_item_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cost_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='selling_price',
        ),
        migrations.AddField(
            model_name='product',
            name='carton_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_quantity',
            field=models.IntegerField(default=1),
        ),
    ]

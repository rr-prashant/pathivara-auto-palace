# Generated by Django 4.2.4 on 2023-08-10 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0008_alter_stock_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='Date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='Date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

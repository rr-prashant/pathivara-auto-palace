# Generated by Django 4.2.4 on 2023-08-10 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0004_servicerequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Part_Number', models.CharField(max_length=100)),
                ('Unit_Price', models.FloatField()),
                ('Quantity', models.PositiveIntegerField()),
                ('Total_Amount', models.FloatField()),
                ('Date', models.DateField(auto_now_add=True)),
                ('Part_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Garage.stock')),
            ],
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-12 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0012_jobcard_stockbill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Picture', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Pathivara_infos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Admin_name', models.CharField(max_length=100)),
                ('Website_name', models.CharField(max_length=100, null=True)),
                ('Website_desc', models.CharField(max_length=1000, null=True)),
                ('Admin_phonenumber', models.CharField(max_length=100, null=True)),
                ('Admin_address', models.CharField(max_length=100, null=True)),
                ('Admin_email', models.CharField(max_length=100, null=True)),
                ('Opening_hours', models.CharField(max_length=100, null=True)),
                ('copyright', models.CharField(max_length=100, null=True)),
                ('Service_desc', models.CharField(max_length=1000, null=True)),
                ('facebook_link', models.CharField(max_length=500, null=True)),
                ('googlemap_link', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_icon', models.ImageField(upload_to='')),
                ('service_title', models.CharField(max_length=100)),
            ],
        ),
    ]

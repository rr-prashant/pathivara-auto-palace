# Generated by Django 4.2.4 on 2023-09-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0026_alter_servicerequest_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='Follow_up_Status',
            field=models.CharField(blank=True, choices=[('Follow_up_Pending', 'FOLLOW_UP_PENDING'), ('Follow_up_Done', 'FOLLOW_UP_DONE')], default='Follow_up_Pending', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='Remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]

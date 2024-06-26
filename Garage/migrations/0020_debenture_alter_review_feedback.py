# Generated by Django 4.2.4 on 2023-09-01 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0019_rename_order_status_review_review_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debenture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Debenture_type', models.CharField(choices=[('Credit', 'CREDIT'), ('Debit', 'DEBIT')], default=' ', max_length=20)),
                ('Amount', models.PositiveIntegerField()),
                ('Date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Reason', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='Feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]

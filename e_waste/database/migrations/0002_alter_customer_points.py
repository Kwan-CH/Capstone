# Generated by Django 5.1.6 on 2025-03-19 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='points',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

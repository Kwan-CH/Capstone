# Generated by Django 5.1.7 on 2025-03-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_pickuprequest_rejectedreason_alter_customer_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickuprequest',
            name='trackingnumber',
            field=models.CharField(default='#JAS2025-0000', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='pickuprequest',
            name='rejectedReason',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]

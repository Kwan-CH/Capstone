# Generated by Django 5.1.6 on 2025-03-26 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_alter_pickeduprequest_requestid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedrequest',
            name='requestID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.schedulerequest'),
        ),
    ]

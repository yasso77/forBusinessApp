# Generated by Django 5.0.4 on 2024-06-22 16:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0013_alter_applicantonjobs_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribers',
            name='createddate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='subscribers',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='subscribers',
            name='inactivateddate',
            field=models.DateField(blank=True, null=True),
        ),
    ]

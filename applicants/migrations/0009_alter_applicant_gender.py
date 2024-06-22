# Generated by Django 5.0.4 on 2024-06-19 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0008_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True, verbose_name='Gender'),
        ),
    ]
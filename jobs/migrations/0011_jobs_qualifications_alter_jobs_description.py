# Generated by Django 5.0.4 on 2024-06-19 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_alter_jobs_contracttype_alter_jobs_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='qualifications',
            field=models.TextField(null=True, verbose_name='Qualifications'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='description',
            field=models.TextField(null=True, verbose_name='Job Description'),
        ),
    ]
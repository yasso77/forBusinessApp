# Generated by Django 5.0.4 on 2024-06-20 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0010_remove_applicantonjobs_applicantid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantonjobs',
            name='coverletter',
            field=models.TextField(max_length=7000, null=True, verbose_name='Cover Letter'),
        ),
    ]
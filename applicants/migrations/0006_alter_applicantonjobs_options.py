# Generated by Django 5.0.4 on 2024-06-18 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0005_remove_applicantonjobs_fitdate_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicantonjobs',
            options={'verbose_name': 'Applicant on Jobs', 'verbose_name_plural': 'Applicants List on jobs'},
        ),
    ]

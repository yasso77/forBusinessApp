# Generated by Django 5.0.4 on 2024-06-18 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0007_remove_applicantonjobs_isview_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscribers',
            fields=[
                ('subscriberid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=155, null=True, verbose_name='Email')),
                ('inactivateddate', models.DateField()),
            ],
            options={
                'verbose_name': 'Subcriber',
                'verbose_name_plural': 'Subcribers List',
            },
        ),
    ]
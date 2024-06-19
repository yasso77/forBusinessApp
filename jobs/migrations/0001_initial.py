# Generated by Django 5.0.4 on 2024-06-17 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('jobid', models.AutoField(primary_key=True, serialize=False, verbose_name='job ID')),
                ('jobtitle', models.CharField(max_length=255, verbose_name='Job Name')),
                ('companyfield', models.CharField(max_length=225)),
                ('jobfield', models.CharField(max_length=225)),
                ('description', models.TextField(null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('nationality', models.CharField(max_length=225)),
                ('placeofwork', models.CharField(max_length=225)),
                ('contracttype', models.CharField(blank=True, choices=[('P', 'Permananet'), ('C', 'Contract')], max_length=1, null=True)),
                ('salary', models.FileField(null=True, upload_to='applicant/cvs/%y/%m/%d')),
                ('eductiondegree', models.CharField(max_length=225)),
                ('experienceyears', models.IntegerField()),
                ('createddate', models.DateField()),
                ('createdby', models.IntegerField()),
            ],
        ),
    ]

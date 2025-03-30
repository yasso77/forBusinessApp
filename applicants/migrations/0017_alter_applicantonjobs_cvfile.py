# Generated by Django 5.0.4 on 2024-06-27 23:34

import pages.commonFun
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0016_alter_applicantonjobs_cvfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantonjobs',
            name='cvFile',
            field=models.FileField(null=True, upload_to=pages.commonFun.PathAndRename('applicant/cvs/'), verbose_name='Upload CV'),
        ),
    ]

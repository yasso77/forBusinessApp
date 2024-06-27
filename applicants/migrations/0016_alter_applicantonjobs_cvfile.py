# Generated by Django 5.0.4 on 2024-06-27 12:13

import pages.commonFun
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0015_alter_subscribers_createddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantonjobs',
            name='cvFile',
            field=models.FileField(null=True, upload_to=pages.commonFun.PathAndRename('applicants/cvs/'), verbose_name='Upload CV'),
        ),
    ]

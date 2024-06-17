from django.db import models
from django.core.validators import RegexValidator

import jobs
# Create your models here.

class Applicant(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    applicantID=models.AutoField(primary_key=True,verbose_name='Applicant ID')
    fullName=models.CharField(max_length=255,verbose_name='Applicant Name')
    email=models.CharField(max_length=155,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    mobile = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$', 'Enter a valid mobile number.')], null=False, blank=False,default=000)  # 
    cvFile=models.FileField(upload_to='applicant/cvs/%y/%m/%d',null=True)
    password=models.CharField(max_length=225,null=False)
    createddate=models.DateField()
    lastlogin=models.DateTimeField()
    addedby=models.CharField()

    def __str__(self) -> str:
        return self.fullName
   
   
class ApplicantOnJobs(models.Model):
       
    incrID=models.AutoField(primary_key=True)
    applicantID=models.ForeignKey(Applicant,on_delete=models.PROTECT)
    jobid=models.ForeignKey(jobs,on_delete=models.PROTECT)
    applydate=models.DateTimeField()
    isview=models.BooleanField()
    isfit=models.BooleanField()
    viewdate=models.DateTimeField()
    fitdate=models.DateTimeField()
    
    def __str__(self) -> str:
        return self.fullName
       
       




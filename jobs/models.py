from django.db import models

# Create your models here.

class Jobs(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    Contract_types=[
        ('P','Permananet'),
        ('C', 'Contract'),
    ]
    
    jobid=models.AutoField(primary_key=True,verbose_name='job ID')
    jobtitle=models.CharField(max_length=255,verbose_name='Job Name')
    companyfield=models.CharField(max_length=225)
    jobfield=models.CharField(max_length=225)
    description=models.TextField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    nationality=models.CharField(max_length=225,null=False)
    placeofwork=models.CharField(max_length=225)
    contracttype=models.CharField(max_length=1, choices=Contract_types, null=True, blank=True)
    salary=models.FileField(upload_to='applicant/cvs/%y/%m/%d',null=True)
    eductiondegree=models.CharField(max_length=225)
    experienceyears=models.IntegerField()
    createddate=models.DateField()
    createdby=models.IntegerField()

    def __str__(self) -> str:
        return self.fullName


from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
from pages.commonFun import CommonFunctions
from jobs.models import Jobs  # Import the Job model from the jobs module


# Create your models here.

# class Applicant(models.Model):        
#     applicantID=models.AutoField(primary_key=True,verbose_name='Applicant ID')
#     fullName=models.CharField(max_length=255,verbose_name='Applicant Name')
#     email=models.CharField(max_length=155,null=True,verbose_name='Email')
#     gender = models.CharField(max_length=10, choices=CommonFunctions.genderList(),null=True, blank=True,verbose_name='Gender')
#     mobile = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$', 'Enter a valid mobile number.')], null=False, blank=False,default=000,verbose_name='Mobile Number')  # 
#     cvFile=models.FileField(upload_to='applicant/cvs/%y/%m/%d',null=True,verbose_name='Upload CV')
#     #password=models.CharField(max_length=225,null=False,verbose_name='Password')
#     createddate=models.DateField(verbose_name="Created Date", auto_now_add=True)
#     #lastlogin=models.DateTimeField()

#     def __str__(self) -> str:
#         return self.fullName
    
#     class Meta:
#         verbose_name = "Applicant"
#         verbose_name_plural = "Applicants List"
   
   
class ApplicantOnJobs(models.Model):
           
    incrID=models.AutoField(primary_key=True)
    jobid=models.ForeignKey(Jobs,on_delete=models.PROTECT,verbose_name='Job Code')
    #applicantID=models.ForeignKey(Applicant,on_delete=models.PROTECT,verbose_name='Applicant Name')
    fullName=models.CharField(max_length=255,null=True,verbose_name='Applicant Name')
    email=models.CharField(max_length=155,null=True,verbose_name='Email')
    gender = models.CharField(max_length=10, choices=CommonFunctions.genderList(),null=True, blank=True,verbose_name='Gender')
    mobile = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$', 'Enter a valid mobile number.')], null=True, blank=False,verbose_name='Mobile Number')
    coverletter=models.TextField(max_length=7000,null=True,verbose_name='Cover Letter')
    cvFile=models.FileField(upload_to='applicant/cvs/%y/%m/%d',null=True,verbose_name='Upload CV')
    applydate=models.DateTimeField(verbose_name="Apply Date", auto_now_add=True)   
    isfit=models.BooleanField(verbose_name='Is fit or no?',null=True)  

    
    def __str__(self):
        return f"{self.fullName} applied for {self.jobid}"
       
    class Meta:
        verbose_name = "Applicant on Jobs"
        verbose_name_plural = "Applicants List on jobs"  

class subscribers(models.Model):
    subscriberid = models.AutoField(primary_key=True,verbose_name='Subscription ID')
    email = models.CharField(max_length=155, null=True, unique=True, verbose_name='Email')
    createddate = models.DateField(default=timezone.now,verbose_name='Subcribe Date')
    isactive = models.BooleanField(default=True,verbose_name='Active Or Not')
    inactivateddate = models.DateField(null=True, blank=True,verbose_name='Inactivation Date')
    
    class Meta:
        verbose_name="Subcriber"
        verbose_name_plural="Subcribers List"



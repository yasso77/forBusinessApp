from django.db import models
from django.core.validators import RegexValidator
from pages.commonFun import CommonFunctions

# Create your models here.

class Recruiters(models.Model):    
       
    recruiterid=models.AutoField(primary_key=True,  verbose_name="Recruiter ID")
    recruitername=models.CharField(max_length=225, verbose_name="Recruiter Name")
    contactperson=models.CharField(max_length=225,null=True, verbose_name="Contact Person")
    email=models.CharField(max_length=155,null=True)
    telephone = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$', 'Enter a valid telephone number.')], null=False, blank=False,default=000)
    locatedin=models.CharField(max_length=100,choices=CommonFunctions.countryList(),verbose_name='Country Located')
    businessfield=models.CharField(max_length=200,verbose_name='Business Field')
    description=models.TextField(max_length=225,verbose_name='Description',null=True)   
    recruiterlogo=models.ImageField(upload_to='recruiter/logo/%y/%m/%d',null=True,verbose_name='Logo')   
    createddate=models.DateField(verbose_name="Created Date", auto_now_add=True)
    isactive=models.BooleanField(verbose_name='Active',default=True)
    
    
    
    def __str__(self) -> str:
        return self.recruitername
    
    class Meta:
        verbose_name = "Recruiter"
        verbose_name_plural = "Recruiters List"
        
        
                
class Jobs(models.Model):    
    
    jobid=models.AutoField(primary_key=True,verbose_name='job ID')
    jobcode=models.CharField(max_length=100,null=True,verbose_name='Job Code')
    jobtitle=models.CharField(max_length=255,verbose_name='Job Name')
    recruiterid=models.ForeignKey(Recruiters,on_delete=models.PROTECT,default=1,verbose_name='Recruiter Name')
    jobfield=models.CharField(max_length=225,verbose_name='Job Field')
    description=models.TextField(null=True, verbose_name='Job Description')
    qualifications=models.TextField(null=True, verbose_name='Qualifications')
    gender = models.CharField(max_length=10, choices=CommonFunctions.genderList(), null=True, blank=True,verbose_name='Gender required')
    nationality=models.CharField(max_length=225,null=False,choices=CommonFunctions.countryList(),verbose_name='Nationality')
    placeofwork=models.CharField(max_length=225,null=True,verbose_name='Job Location')
    contracttype=models.CharField(max_length=100, choices=CommonFunctions.contractTypes(), null=True, blank=True,verbose_name='Contract type')
    salary=models.CharField(max_length=225,null=True,verbose_name='Expeceted Salary')
    eductiondegree=models.CharField(max_length=225,verbose_name='Eductaion')
    experienceyears=models.IntegerField(verbose_name='Number of Experince')
    validdate=models.DateField(null=True,verbose_name="Valid Till")
    createddate=models.DateField(null=True,verbose_name="Created Date", auto_now_add=True)
   

    def __str__(self) -> str:
        return self.jobtitle    
    
    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs List" 

    


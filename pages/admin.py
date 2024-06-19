from django.contrib import admin
from django.utils import timezone
from jobs.models import Jobs,Recruiters
from applicants.models import Applicant,ApplicantOnJobs
from django.utils.html import format_html
# Register your models here.



# Register your models here.
class ApplicantAdmin(admin.ModelAdmin):
    list_display=['applicantID','fullName','gender','mobile','email','download_cv',]
    list_display_links=['fullName']   
    search_fields=['fullName','mobile']
    exclude = ['createddate']  # List the fields you want to exclude  
      
    def download_cv(self, obj):
        if obj.cvFile:
            return format_html('<a href="{}" download>Download CV</a>', obj.cvFile.url)
        return "No CV"
    download_cv.short_description = 'Uploaded CV'
         
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (not updated)
             obj.createddate = timezone.now().date()
        super().save_model(request, obj, form, change)
        


class ApplicantOnJobsAdmin(admin.ModelAdmin):
    list_display=['jobid','job_title','recruiter_name','applicantID','download_cv','applydate','isfit']
      
    def job_title(self, obj):
        return obj.jobid.jobtitle
    job_title.short_description = 'Job Title'
    
    exclude = ['createddate']  # List the fields you want to exclude   
    
    def recruiter_name(self, obj):        
        return obj.jobid.recruiterid
    recruiter_name.short_description = 'Recruiter Name'
    
    def download_cv(self, obj):
        cv=obj.applicantID.cvFile
        if cv:
            return format_html('<a href="{}" download>Download CV</a>', cv.url)
        return "No CV"   
    download_cv.short_description = 'Attched CV'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (not updated)
             obj.applydate = timezone.now().date()
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Applicant,ApplicantAdmin)
admin.site.register(ApplicantOnJobs,ApplicantOnJobsAdmin)

class JobsAdmin(admin.ModelAdmin):
    list_display=['jobcode','jobtitle','jobfield','recruiterid','contracttype','createddate','validdate']
    list_display_links=['jobcode']
    #list_editable=['mobile']
    search_fields=['jobcode','recruiterid','jobtitle']
   # list_filter=['mobile']
    #list_per_page=2
    #fields=['fileserial','fullname','birthdate']
    exclude = ['createddate']  # List the fields you want to exclude    
    
         
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (not updated)
             obj.createddate = timezone.now().date()
        super().save_model(request, obj, form, change)
    
    
    
class RecruitersAdmin(admin.ModelAdmin):
    list_display = ('recruiterid','recruitername','recruiter_logo' ,'locatedin','businessfield','isactive', 'createddate')
    list_display_links=['recruitername']
    exclude = ['createddate']  # List the 
    
    def recruiter_logo(self, obj):
        if obj.recruiterid.recruiterlogo:
            return format_html('<img src="{}" width="100" />', obj.recruiterid.recruiterlogo.url)
        return "No Logo"
    recruiter_logo.short_description = 'Recruiter Logo'
        
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (not updated)
             obj.createddate = timezone.now().date()
        super().save_model(request, obj, form, change)

admin.site.register(Jobs,JobsAdmin)
admin.site.register(Recruiters,RecruitersAdmin)
# Register your models here.
admin.site.site_header='ForBusiness-Administration'
admin.site.site_title='4BUS-Group'
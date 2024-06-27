from django.urls import path, reverse
from django.contrib import admin
from django.shortcuts import render
from django.utils import timezone
from jobs.models import Jobs,Recruiters
from applicants.models import ApplicantOnJobs,subscribers
from django.utils.html import format_html

from pages.ormQuery import jobQueries
from django.db.models import Q
# Register your models here.



# Register your models here.
# class ApplicantAdmin(admin.ModelAdmin):
#     list_display=['applicantID','fullName','gender','mobile','email','download_cv',]
#     list_display_links=['fullName']   
#     search_fields=['fullName','mobile']
#     exclude = ['createddate']  # List the fields you want to exclude  
      
#     def download_cv(self, obj):
#         if obj.cvFile:
#             return format_html('<a href="{}" download>Download CV</a>', obj.cvFile.url)
#         return "No CV"
#     download_cv.short_description = 'Uploaded CV'
         
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # If the object is being created (not updated)
#              obj.createddate = timezone.now().date()
#         super().save_model(request, obj, form, change)
        


class ApplicantOnJobsAdmin(admin.ModelAdmin):
    list_display=['jobcode','jobtitle','recruiter_name','fullName','mobile','download_cv','applydate','isfit']   
    list_display_links=['fullName']   
    search_fields = ['fullName', 'mobile', 'jobid__jobtitle', 'jobid__jobcode', 'jobid__recruiterid__recruitername']
    exclude = ['createddate']  # List the fields you want to exclude  
    
    def jobtitle (self, obj):
        return obj.jobid.jobtitle
    jobtitle.short_description = 'Job Title'
    
    def jobcode (self, obj):
        return obj.jobid.jobcode
    jobcode.short_description = 'Job Code'
    
    exclude = ['createddate']  # List the fields you want to exclude   
    
    def recruiter_name(self, obj):        
        return obj.jobid.recruiterid
    recruiter_name.short_description = 'Recruiter Name'
    
    def download_cv(self, obj):
        cv=obj.cvFile
        if cv:
            return format_html('<a href="{}" download>Download CV</a>', cv.url)
        return "No CV"   
    download_cv.short_description = 'Attached CV'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (not updated)
             obj.applydate = timezone.now().date()
        super().save_model(request, obj, form, change)

class SubcribersAdmin(admin.ModelAdmin):
    list_display=['subscriberid','email','createddate','isactive','inactivateddate']   
    #list_display_links=['fullName']   
    search_fields = ['email', 'createddate']
# Register your models here.
#admin.site.register(ApplicantAdmin)
admin.site.register(ApplicantOnJobs,ApplicantOnJobsAdmin)
admin.site.register(subscribers,SubcribersAdmin)

class JobsAdmin(admin.ModelAdmin):
    list_display=['jobcode','jobtitle','jobfield','applicant_count','recruiterid','contracttype','createddate','validdate']
    list_display_links=['jobcode']
    #list_editable=['mobile']
    search_fields=['jobcode','recruiterid','jobtitle']
   # list_filter=['mobile']
    #list_per_page=2
    #fields=['fileserial','fullname','birthdate']
    exclude = ['createddate']  # List the fields you want to exclude    
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('applicants/<int:job_id>/', self.admin_site.admin_view(self.applicant_list), name='applicant_list'),
        ]
        return custom_urls + urls

    def applicant_list(self, request, job_id):
        job = jobQueries.get_jobDetails(job_id)
        if not job:
            return render(request, 'job_not_found.html', {'jobid': job_id})
        
        search_query = request.GET.get('q', '')
        if search_query:
            applicants = ApplicantOnJobs.objects.filter(
                Q(fullName__icontains=search_query) | 
                Q(mobile__icontains=search_query) | 
                Q(email__icontains=search_query) | 
                Q(gender__icontains=search_query) | 
                Q(coverletter__icontains=search_query),
                jobid=job_id
            )
        else:
            applicants = ApplicantOnJobs.objects.filter(jobid=job_id)

        return render(request, 'admin/applicant_list.html', {'job': job, 'applicants': applicants, 'search_query': search_query})
    
    def applicant_count(self, obj):
        count = ApplicantOnJobs.objects.filter(jobid=obj).count()
        url = reverse('admin:applicant_list', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, count)
    applicant_count.short_description = 'Number of Applicants'

 
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (not updated)
             obj.createddate = timezone.now().date()
        super().save_model(request, obj, form, change)
    
    
    
class RecruitersAdmin(admin.ModelAdmin):
    list_display = ('recruiter_logo','recruitername','locatedin','businessfield','isactive', 'createddate')
    list_display_links=['recruitername']
    exclude = ['createddate']  # List the 
    
    def recruiter_logo(self, obj):
        if obj.recruiterlogo:
            return format_html('<img src="{}" width="75" />', obj.recruiterlogo.url)
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
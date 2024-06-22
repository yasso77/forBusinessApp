from django.utils import timezone
from jobs.models import Jobs,Recruiters
from applicants.models import ApplicantOnJobs


class jobQueries():
    def get_active_jobs():
       
        # Getting the current date
        today = timezone.now().date()

        # Querying Jobs with conditions and including related Recruiters fields
        jobsList = Jobs.objects.filter(validdate__gt=today, recruiterid__isactive=True).select_related('recruiterid').values(
            'jobid', 'jobcode','contracttype', 'jobtitle','salary','placeofwork', 'validdate', 'createddate',
            'recruiterid__recruitername', 'recruiterid__recruiterlogo'
        )
        
        return jobsList
    
    def get_jobDetails(jobid):
        jobdetails = Jobs.objects.filter(jobid=jobid).select_related('recruiterid').values(
        'jobid', 'jobcode','qualifications','description', 'contracttype', 'jobtitle', 'salary', 'placeofwork', 'validdate', 'createddate',
        'recruiterid__recruitername', 'recruiterid__recruiterlogo'
    ).first()
        return jobdetails
    
    def get_jobInstance(jobid):
        jobinstance = Jobs.objects.filter(jobid=jobid).first()
        return jobinstance
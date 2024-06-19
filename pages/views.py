from django.shortcuts import render
from pages.ormQuery import jobQueries

# Create your views here.

def index(request):
       return render(request, 'index.html')

def contact(request):
       return render(request, 'contact.html')

def jobsList(request):
       activeJobList= jobQueries.get_active_jobs()
       return render(request,'jobs.html',{'jobList':activeJobList})

def jobDetails(request,jobid):
       jobdetail= jobQueries.get_jobDetails(jobid)
       if not jobdetail:
           # Handle the case where no job is found
           return render(request, 'job_not_found.html', {'jobid': jobid})
              
       return render(request,'job-details.html',{'job':jobDetails})

def about(request):
       return render(request,'about.html')
def faq(request):
       return render(request,'faq.html')

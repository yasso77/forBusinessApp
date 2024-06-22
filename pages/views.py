from datetime import date
from django.shortcuts import redirect, render
from forBusinessWepApp import settings
from pages.applicantform import applicantForm
from pages.ormQuery import jobQueries
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

def index(request):
       return render(request, 'index.html')

def contact(request):
       return render(request, 'contact.html')

def jobsList(request):
       activeJobList= jobQueries.get_active_jobs()
       return render(request,'jobs.html',{'jobList':activeJobList})

def jobDetails(request, jobid):
    # Fetch the job details
    job = jobQueries.get_jobDetails(jobid)
    
    if not job:
        # Handle the case where no job is found
        return render(request, 'job_not_found.html', {'jobid': jobid})
    # Get the Jobs instance
    job_instance = jobQueries.get_jobInstance(jobid)
    
    if request.method == 'POST':
        form = applicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant_on_job = form.save(commit=False)
            applicant_on_job.jobid = job_instance  # Assign the Jobs instance
            applicant_on_job.applydate = date.today()  # Set the apply date
            applicant_on_job.save()
            return redirect(reverse('message', args=['Your application on the job is submitted successfully, we will be in contact with you']))  # Change 'success_url' to the actual URL name
    else:
        form = applicantForm(initial={'jobid': job['jobid']})
    
    return render(request, 'job-details.html', {'job': job, 'form': form})

def about(request):
       return render(request,'about.html')
def faq(request):
       return render(request,'faq.html')

def message(request,strmessage):
       return render(request,'message.html',{'msg':strmessage})

def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'error.html', {'error': 'Invalid email format.'})
        
        # Email subject and content
        subject = f'New Contact Form Submission from {name}'
        message_content = render_to_string('contact_form_email.html', {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
        })
        
        # Send email
        send_mail(subject, message_content, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
        
        # Redirect after successful submission
        return redirect(reverse('message', args=['Your Inquery is sent successfully']))
    
    return render(request, 'error.html', {'error': 'Method not allowed.'})
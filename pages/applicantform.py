# forms.py
from datetime import date, datetime
from django import forms
from applicants.models import ApplicantOnJobs
from django.core.validators import FileExtensionValidator
import re

class applicantForm(forms.ModelForm):   
    
    coverletter = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), max_length=7000, help_text="Max 7000 characters")
    
    cvFile = forms.FileField(label='Upload CV', validators=[FileExtensionValidator(allowed_extensions=['docx', 'doc', 'pdf'])], required=True)  
    
    class Meta:
        model = ApplicantOnJobs
        fields = ['fullName', 'mobile','gender','email','coverletter','jobid', 'cvFile']
        jobid = forms.IntegerField(widget=forms.HiddenInput())
        #file_upload = forms.FileField(required=True)
        
        
        widgets = {
            'fullName': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
            'jobid': forms.HiddenInput(),       
    
        }
        error_messages = {
           
            'fullName': {
                'required': 'Full name is required.',
            },
            'mobile': {
                'required': 'Mobile number is required.',
            },          
          
            'gender': {
                'required': 'Gender is required.',
            },
            'email': {
                'required': 'Suffered case is required.',
                'invalid': 'Enter a valid email address.',
            },
            'cvFile':{
                'required':'CV file is required',
            }
            
          }
        
    def __init__(self, *args, **kwargs):
        super(applicantForm, self).__init__(*args, **kwargs)
        self.fields['gender'].choices = [
            ('Male', 'Male'),
            ('Female', 'Female')
        ]
        self.fields['cvFile'].required = True
        
    def validate_email_format(self, value):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise forms.ValidationError('Enter a valid email address.')
        
    def clean(self):
        cleaned_data = super().clean()
        mobile = cleaned_data.get('mobile')
        email = cleaned_data.get('email')
        jobid = cleaned_data.get('jobid')

        if ApplicantOnJobs.objects.filter(mobile=mobile, email=email, jobid=jobid).exists():
            raise forms.ValidationError('You applied for this job before.')

        return cleaned_data
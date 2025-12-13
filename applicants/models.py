from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator
from pages.commonFun import CommonFunctions,PathAndRename
from jobs.models import Jobs  # Import the Job model from the jobs module


# Create your models here.

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Applicant(models.Model):
    # =========================
    # Primary Key
    # =========================
    applicantID = models.AutoField(
        primary_key=True,
        verbose_name=_("Applicant ID")
    )

    # =========================
    # Personal Information
    # =========================
    fullName = models.CharField(
        max_length=255,
        verbose_name=_("Full Name"),
        help_text=_("Full name as extracted from CV (Arabic or English)")
    )

    fullNameNormalized = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Normalized Name"),
        help_text=_("Name normalized for search (no diacritics, lowercase)")
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_("Email Address")
    )

    mobile = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(
                r'^\+?\d{7,20}$',
                _("Enter a valid mobile number")
            )
        ],
        null=True,
        blank=True,
        verbose_name=_("Mobile Number")
    )

    gender = models.CharField(
        max_length=10,
        choices=(
            ('Male', _('Male')),
            ('Female', _('Female')),
        ),
        null=True,
        blank=True,
        verbose_name=_("Gender")
    )

    # =========================
    # Language & Localization
    # =========================
    cvLanguage = models.CharField(
        max_length=20,
        choices=(
            ('Arabic', _('Arabic')),
            ('English', _('English')),
            ('Mixed', _('Mixed')),
            ('Unknown', _('Unknown')),
        ),
        default='Unknown',
        verbose_name=_("CV Language")
    )

    # =========================
    # Professional Information
    # =========================
    jobTitle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Current / Last Job Title")
    )

    yearsOfExperience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name=_("Years of Experience")
    )

    skills = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Skills"),
        help_text=_("Comma-separated or JSON list of skills")
    )

    languages = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Spoken Languages"),
        help_text=_("Arabic, English, French, etc.")
    )

    # =========================
    # Location & Mobility
    # =========================
    currentCountry = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Current Country")
    )

    currentCity = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Current City")
    )

    targetCountry = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Target Country for Work")
    )

    availability = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Availability")
    )

    # =========================
    # Education
    # =========================
    educationLevel = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Education Level")
    )

    lastUniversity = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("University / Institute")
    )

    # =========================
    # CV Storage & Parsing
    # =========================
    cvFile = models.FileField(
        upload_to='applicant/cvs/%Y/%m/',
        verbose_name=_("CV File")
    )

    cvOriginalFileName = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original CV File Name"),
        help_text=_("Original file name (Arabic or English)")
    )

    cvText = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Extracted CV Text"),
        help_text=_("Full extracted text from CV (Arabic + English)")
    )

    cvTextNormalized = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Normalized CV Text"),
        help_text=_("Normalized text for fast search (Arabic/English cleaned)")
    )

    parsedStatus = models.BooleanField(
        default=False,
        verbose_name=_("Parsed Successfully")
    )

    parsingErrors = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Parsing Errors / Notes")
    )

    # =========================
    # Source & Tracking
    # =========================
    source = models.CharField(
        max_length=100,
        default="Local CV Import",
        verbose_name=_("Source")
    )

    # =========================
    # Audit Fields
    # =========================
    createdDate = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created Date")
    )

    updatedDate = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Updated")
    )

    lastReviewedByRecruiter = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Reviewed By Recruiter")
    )

    isActive = models.BooleanField(
        default=True,
        verbose_name=_("Active Candidate")
    )
    
    aiConfidence = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("AI Confidence Score"   )
    )


    # =========================
    # Model Meta
    # =========================
    class Meta:
        verbose_name = _("Applicant")
        verbose_name_plural = _("Applicants")
        indexes = [
            models.Index(fields=['fullName']),
            models.Index(fields=['mobile']),
            models.Index(fields=['email']),
            models.Index(fields=['jobTitle']),
            models.Index(fields=['targetCountry']),
        ]

    def __str__(self):
        return f"{self.fullName} ({self.mobile})"

class ApplicantOnJobs(models.Model):
        # Usage
    path_and_rename = PathAndRename("applicant/cvs/")
           
    incrID=models.AutoField(primary_key=True)
    jobid=models.ForeignKey(Jobs,on_delete=models.PROTECT,verbose_name='Job Code')
    #applicantID=models.ForeignKey(Applicant,on_delete=models.PROTECT,verbose_name='Applicant Name')
    fullName=models.CharField(max_length=255,null=True,verbose_name='Applicant Name')
    email=models.CharField(max_length=155,null=True,verbose_name='Email')
    gender = models.CharField(max_length=10, choices=CommonFunctions.genderList(),null=True, blank=True,verbose_name='Gender')
    mobile = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$', 'Enter a valid mobile number.')], null=True, blank=False,verbose_name='Mobile Number')
    coverletter=models.TextField(max_length=7000,null=True,verbose_name='Cover Letter')
    cvFile = models.FileField(upload_to=path_and_rename, null=True, verbose_name='Upload CV')
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



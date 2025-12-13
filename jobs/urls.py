from django.urls import path
from .views import job_detail_api

urlpatterns = [
    path('api/job-detail/', job_detail_api, name='job_detail_api'),
]

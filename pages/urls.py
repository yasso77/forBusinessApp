from django.urls import path
from pages import views

urlpatterns = [
     path('', views.index, name='index'),
     path('contact', views.contact, name='contact'),
     path('jobs', views.jobsList, name='jobs'),
     path('jobdetail/<int:jobid>/',views.jobDetails,name='jobdetails'),    
     path('about', views.about, name='about'),
     path('faq', views.faq, name='faq'),
     
]
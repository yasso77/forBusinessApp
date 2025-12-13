from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Jobs
from .serializers import JobSerializer  # You'll create this below

# Dummy token for example
VALID_TOKEN = 'forbusiness@com.api.jobdetails'

@api_view(['GET'])
@permission_classes([AllowAny])  # Adjust if using authenticated users
def job_detail_api(request):
    job_code = request.GET.get('jobcode')
    token = request.GET.get('token')

    if token != VALID_TOKEN:
        return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        job = Jobs.objects.get(jobcode=job_code)
        serializer = JobSerializer(job)
        return Response(serializer.data)
    except Jobs.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

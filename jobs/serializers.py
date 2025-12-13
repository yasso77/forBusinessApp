from rest_framework import serializers
from .models import Jobs

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = [
            'jobcode', 'jobtitle', 'recruiterid', 'jobfield', 'description',
            'qualifications', 'gender', 'nationality', 'placeofwork',
            'contracttype', 'salary', 'eductiondegree', 'experienceyears',
            'validdate', 'createddate'
        ]

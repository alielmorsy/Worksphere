from rest_framework import serializers

from .abstract_models import CompanyUser
from .models import Company, Task
from userAuth.auth import User
from .exceptions import UserNotExists,TaskNotExists
from bson import ObjectId ,objectid

class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("companyName",)

    def create(self, validated_data):
        company_owner = validated_data["company_owner"]
        company = Company.objects.create(companyName=validated_data["companyName"], companyOwner=company_owner)
        return company

        
class CreateTaskSerializer(serializers.ModelSerializer):
    assignedTo = serializers.ListSerializer(child=serializers.CharField(allow_blank=False), required=False) 
    reviewers  = serializers.ListSerializer(child=serializers.CharField(allow_blank=True), required=False)
    assignedTask = serializers.CharField( required=False , allow_blank=True)
    def create(self, validated_data , request):
        user = request.user
        createdBy = CompanyUser.objects.get(user=user)
        task = Task.objects.create(taskName=validated_data['taskName']   ,   taskDescription=validated_data['taskDescription'] , 
                                   createdBy=createdBy)
        print(validated_data['assignedTo'])
        for user in validated_data['assignedTo']:
            task.assignedTo.add(user)
        for user in validated_data['reviewers']:
            task.reviewers.add(user)
        task.save()
        try:
            assignedTask = validated_data['assignedTask']
            assignedTask.subTasks.add(task)
            assignedTask.save()
        except:
            pass
        return task

    def validate_assignedTo(self, assignedTo):
        try:
            return [ CompanyUser.objects.get(pk=ObjectId(userid)) for userid in assignedTo ]
        except:
            raise UserNotExists()
        
    def validate_reviewers(self, reviewers):
        try:
            return [ CompanyUser.objects.get(pk=ObjectId(userid)) for userid in reviewers ]
        except:
            raise UserNotExists()
        
    def validate_assignedTask(self, assignedTask):
        try:
            return Task.objects.get(pk=ObjectId(assignedTask))
        except:
            raise TaskNotExists()

    class Meta:
        model = Task
        fields = ["taskName", "taskDescription", "assignedTo", "reviewers",  "assignedTask", ]
        read_only_fields = ('_id',)
from rest_framework import serializers

from .models import Company, Task
from userAuth.auth import User
from .exceptions import UserNotExists,TaskNotExists
from bson import objectid

class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("companyName",)

    def create(self, validated_data):
        company_owner = validated_data["company_owner"]
        company = Company.objects.create(companyName=validated_data["companyName"], companyOwner=company_owner)
        return company


class AssignedToListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        try:
            return [ User.objects.get(pk=objectid(userid)) for userid in attrs ]
        except:
            raise UserNotExists()

class ReviewersListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        try:
            return [ User.objects.get(pk=objectid(userid)) for userid in attrs ]
        except:
            raise UserNotExists()
            
        
class CreateTaskSerializer(serializers.ModelSerializer):
    assignedTo = AssignedToListSerializer
    reviewers  = ReviewersListSerializer
    assignedTask = serializers.CharField(maxlength=32 , required=False)
    def create(self, validated_data):
        createdBy = self.context.get("request").user
        task = Task.objects.create(taskName=validated_data['taskName']   ,   taskDescription=validated_data['taskDescription'] , 
                                   createdBy=createdBy)
        for userid in validated_data['assignedTo']:
            task.assignedTo.add(User.objects.get(pk=objectid(userid)))
        for userid in validated_data['reviewers']:
            task.reviewers.add(User.objects.get(pk=objectid(userid)))
        task.save()
        try:
            assignedTask = Task.objects.get(pk=objectid(validated_data['assignedTask']))
            assignedTask.subTasks.add(task)
            assignedTask.save()
        except:
            pass
        return task

    def validate_assignedTask(self, assignedTask):
        try:
            assignedTask = Task.objects.get(pk=objectid(assignedTask))
        except:
            raise TaskNotExists()
        return assignedTask

    class Meta:
        model = Task
        fields = ["taskName", "taskDescription", "assignedTo", "reviewers",  "assignedTask", ]
        read_only_fields = ('_id',)
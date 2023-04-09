from rest_framework import serializers

from .models import Company, Task
from userAuth.auth import User
from .exceptions import UserNotExists, TaskNotExists
from bson import ObjectId, ObjectId


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
            return [User.objects.get(pk=ObjectId(userid)) for userid in attrs]
        except:
            raise UserNotExists()


class SubTasksListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        try:
            return [Task.objects.get(pk=ObjectId(task_id)) for task_id in attrs]
        except:
            raise TaskNotExists()


class ReviewersListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        try:
            return [User.objects.get(pk=ObjectId(userid)) for userid in attrs]
        except:
            raise UserNotExists()


class CreateTaskSerializer(serializers.ModelSerializer):
    assignedTo = AssignedToListSerializer
    reviewers = ReviewersListSerializer
    sub_tasks = SubTasksListSerializer

    def create(self, validated_data):
        created_by = validated_data["user"]
        task = Task.objects.create(taskName=validated_data['taskName'],
                                   taskDescription=validated_data['taskDescription'],
                                   createdBy=created_by)
        for userid in validated_data['assignedTo']:
            task.assignedTo.add(ObjectId(userid))
        for userid in validated_data['reviewers']:
            task.reviewers.add(ObjectId(userid))
        task.save()
        try:
            sub_tasks = Task.objects.get(pk=ObjectId(validated_data['sub_tasks']))
            sub_tasks.subTasks.add(task)
            sub_tasks.save()
        except:
            raise RuntimeWarning("Invalid Information")
        return task

    def validate_assignedTask(self, assignedTask):
        try:
            assignedTask = Task.objects.get(pk=ObjectId(assignedTask))
        except:
            raise TaskNotExists()
        return assignedTask

    class Meta:
        model = Task
        fields = ["taskName", "taskDescription", "assignedTo", "reviewers", "sub_tasks", ]
        read_only_fields = ('_id',)

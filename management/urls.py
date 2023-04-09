from django.contrib import admin
from django.urls import path, include

from management.views import CreateNewCompany, CreateTask

urlpatterns = [
    path("company/create", CreateNewCompany.as_view()),
    path("task/create", CreateTask.as_view())
]

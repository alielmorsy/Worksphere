from django.contrib import admin
from django.urls import path, include

from management.views import CreateNewCompany

urlpatterns = [
    path("company/create", CreateNewCompany.as_view())
]

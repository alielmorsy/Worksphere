from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.base import AuthorizedCompanyBase
from management.permission_utils import DoesUserHavePermission, DefaultPermissions
from management.serializers import CreateCompanySerializer, CreateTaskSerializer
from bson import ObjectId
from userAuth.auth import User

class CreateNewCompany(APIView):
    """
    API  request responsible for creating new company which using CreateCompanySerializer to validate
    the request, and create the company and assign the default roles, and the default channel, and save to database.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request ,*args, **kwargs):
        user = request.user
        serializer = CreateCompanySerializer(data=request.data, )
        serializer.is_valid(raise_exception=True)
        company = serializer.save(company_owner=user)
        response = {
            "message": "Company Created Successfully",
            "companyId": str(company)
        }
        return Response(response)


class CreateTask(APIView, AuthorizedCompanyBase):
    default_permissions = DefaultPermissions.CAN_ADD_TASKS
    permission_classes = (IsAuthenticated, DoesUserHavePermission)
    def post(self , request , *args, **kwargs ):
        #request.user = User.objects.get(pk=ObjectId('642759c6e1d5e90be8cf1ab8'))  #cant add authorization data to request so i did this trick to test
        serializer = CreateTaskSerializer(data= request.data,)
        serializer.is_valid(raise_exception=True)
        task = serializer.create(serializer.validated_data , request)
        response = {
            "message": "Task Created Successfully",
            "taskId": str(task._id)
        }
        return Response(response)


        

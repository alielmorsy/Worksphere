
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.serializers import CreateCompanySerializer


class CreateNewCompany(APIView):
    """
    API  request responsible for creating new company which using CreateCompanySerializer to validate
    the request, and create the company and assign the default roles, and the default channel, and save to database.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = CreateCompanySerializer(data=request.data, )
        serializer.is_valid(raise_exception=True)
        company = serializer.save(company_owner=user)
        response = {
            "message": "Company Created Successfully",
            "companyId": str(company)
        }
        return Response(response)

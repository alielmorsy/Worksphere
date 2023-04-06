from bson import ObjectId
from django.shortcuts import render
# Create your views her
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.base import AuthorizedCompanyBase
from management.permission_utils import IsUserInCompany
from .serializer import CreateChannelSerializer, SendMassageSerializer
from .validators import Validate_channel_and_user


class CreateChannelView(APIView, AuthorizedCompanyBase):
    permission_classes = (IsAuthenticated, IsUserInCompany)
    raise_exception = True

    def post(self, request, *args, **kwargs):
        print(request.user)
        serializer = CreateChannelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.create(serializer.validated_data)
        channel.save()
        response = {
            "channel": str(channel.pk),
            "State": 'channel named ' + channel.channelName + ' Created succefully'
        }
        return Response(response)

    def get_company_id(self, request):
        data = request.data
        if "company_id" not in data:
            raise RuntimeError("Bad Request")

        return ObjectId(data["companyId"])


class SendMessageView(APIView):
    raise_exception = True

    def post(self, request, *args, **kwargs):
        serializer = SendMassageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.create(serializer.validated_data)
        message.save()
        response = {
            "message": f"To: {message.sender.username} Body: {message.messageBody}",
        }
        return Response(response)

from bson import ObjectId
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.base import AuthorizedCompanyBase
from management.models import Company
from management.permission_utils import IsUserCompany
from .serializer import CreateChannelSerializer, SendMassageSerializer


class CreateChannelView(APIView, AuthorizedCompanyBase):
    """
    Simple view that works on post only.
    It takes in request
    [channelName,channelType, company_id]
    Company ID is the company to create channel inside it.
    channel Name is the name of the channel.
    ChannelType Type of channel [VOICE, CHAT]
    Then return the channel after create it.
    Checks Done:
        - User are Authenticated
        - Does User Part of company.

    TODO: Check whether the user who created the channel is admin or not.
    TODO: Make the response looks pretty.
    @author Ali Elmorsy
    """
    permission_classes = (IsAuthenticated, IsUserCompany)
    raise_exception = True

    def post(self, request, *args, **kwargs):
        serializer = CreateChannelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.create(serializer.validated_data)
        channel.save()
        response = {
            "channel_id": str(channel.pk),
            "State": 'channel named ' + channel.channelName + ' Created successfully'
        }
        return Response(response)


class GetAllChannels(APIView, AuthorizedCompanyBase):
    """
    When user enters the company chat the first thing should see is all channels in the server. This request is a get
    request that accept `company_id` as url parameter and retrieve all channels in it. Checks Done: - User is
    Authenticated. - User is part of the company.
    TODO: When channel is sent to the user, a new query should be done that checks whether the user is allowed to write or read from that channel or not.

    """
    permission_classes = (IsAuthenticated, IsUserCompany)
    raise_exception = True

    def get(self, request, *args, **kwargs):
        company_id = self.get_company_id(request)
        company = Company.objects.get(_id=company_id)
        channelsObject = company.channels
        channels = []
        for channel_object in channelsObject:
            channel = {"channelName": channel_object.channelName,
                       "channelType": channel_object.channelType,
                       "channelId": str(channel_object.pk)
                       }
            channels.append(channel)
        response = {"companyName": company.companyName,
                    "companyId": str(company_id),
                    "channels": channels
                    }
        return Response(response)

    def get_company_id(self, request):
        company_id = self.kwargs["company_id"]
        return ObjectId(company_id)


# TODO: We don't need that.
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

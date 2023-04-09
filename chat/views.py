from bson import ObjectId
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.base import AuthorizedCompanyBase
from management.models import Company
from management.permission_utils import IsUserCompany, DoesUserHavePermission, DefaultPermissions
from .serializer import CreateChannelSerializer, SendMassageSerializer, GetMessagesSerializer

from django.conf import settings


class CreateChannelView(APIView, AuthorizedCompanyBase):
    """
    Simple view that works on post only.
    It takes in request
    [channelName , channelType , company_id]
    Company ID is the company to create channel inside it.
    channel Name is the name of the channel.
    ChannelType Type of channel [VOICE, CHAT]
    Then return the channel after create it.
    Checks Done:
        - User are Authenticated
        - Does User Part of company.

    TODO: Check whether the user who created the channel is admin or not. (DONE)
    TODO: Make the response looks pretty.
    @author Ali Elmorsy
    """

    default_permissions = DefaultPermissions.CREATE_REMOVE_CHANNELS
    permission_classes = (IsAuthenticated, DoesUserHavePermission)
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


class GetChannelMessagesView(APIView):
    raise_exception = True
    permission_classes = (IsAuthenticated, IsUserCompany)

    def get(self, request):
        serializer = GetMessagesSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        page = data["page"]
        channel_id = data["channel_id"]
        channel = data["channel"]

        messages = []
        query = channel.messages.all()[settings.MESSAGES_PER_PAGE * (page - 1): settings.MESSAGES_PER_PAGE * page]
        for message in query:
            messages.append(message.to_dict())

        response = {
            "channel_id": channel_id,
            "numberOfMessages": len(messages),
            "messages": messages
        }
        return Response(response)

    def get_company_id(self, request):
        company_id = self.kwargs["company_id"]
        return ObjectId(company_id)


class GetAllChannels(APIView, AuthorizedCompanyBase):
    """
    When user enters the company chat the first thing should see is all channels in the server. This request is a get
    request that accept `company_id` as url parameter and retrieve all channels in it. Checks Done: - User is
    Authenticated. - User is part of the company.
    TODO: Big Mistake: The permission check is an issue because i am telling the user that he cannot see all channels if he doesn't have any permission.
    """

    default_permissions = DefaultPermissions.CAN_READ
    permission_classes = (IsAuthenticated, DoesUserHavePermission)
    raise_exception = True

    def get(self, request, *args, **kwargs):
        company_id = self.get_company_id(request)
        company = Company.objects.get(_id=company_id)
        channels_objects = company.channels
        channels = []
        for channel_object in channels_objects:
            channel = {"channelName": channel_object.channelName,
                       "channelType": channel_object.channelType,
                       "channelId": str(channel_object.pk),
                       "totalMessages": len(channel_object.messages)
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

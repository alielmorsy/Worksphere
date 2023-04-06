from rest_framework import serializers

from management.models import Company
from .models import *
from . import models
from rest_framework import serializers
from userAuth.models import User
from .exceptions import UserDoesnotExist, ChannelDoesnotExist
from bson import ObjectId


# create a serializer


class CreateChannelSerializer(serializers.ModelSerializer):
    createdBy = serializers.CharField(max_length=32)

    def create(self, validated_data):
        """
        Custom create function that not only create the channel, it insert it inside the company object.
        """
        channel = Channel.objects.create(createdBy=User.objects.get(username=validated_data['createdBy']),
                                         channelName=validated_data['channelName'],
                                         channelType=validated_data['channelType'])
        channel.save()
        company_id = validated_data["company_id"]
        company = Company.objects.get(_id=ObjectId(company_id))
        company.channels.add(company)
        company.save()
        return channel

    def validate_createdBy(self, createdBy):
        try:
            user = User.objects.get(username=createdBy)
        except:
            raise UserDoesnotExist()
        return user

    class Meta:
        model = Channel
        fields = ["channelName", "channelType", "company_id"]
        read_only_fields = ('_id',)


class SendMassageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=32)
    Channel = serializers.CharField(max_length=32)

    def create(self, validated_data):
        try:
            if validated_data['repliedFrom'] is None:
                replied_from = None
            else:
                replied_from = Message.objects.get(_id=validated_data['repliedFrom'])
        except:
            replied_from = None

        message = Message.objects.create(sender=self.validate_and_get_sender(validated_data['sender']),
                                         messageBody=validated_data['messageBody'],
                                         repliedFrom=replied_from,
                                         )
        self.validate_and_get_channel(validated_data['Channel']).messages.add(message)
        return message

    def validate_and_get_sender(self, sender):
        try:
            user = User.objects.get(username=sender)
        except:
            raise UserDoesnotExist()
        return user

    def validate_and_get_channel(self, Channel):
        # user = User.objects.get(username=username)
        try:
            channel = models.Channel.objects.get(_id=ObjectId(Channel))
        except:
            raise ChannelDoesnotExist()
        return channel

    class Meta:
        model = Message
        fields = ["messageBody", "sender", "repliedFrom", 'Channel']
        read_only_fields = ('_id',)

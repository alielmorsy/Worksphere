import django.db.models
from django.db import models
from django.db.models import CASCADE, DO_NOTHING
from djongo.models import ObjectIdField, ArrayReferenceField
from django.utils.translation import gettext_lazy as _

from userAuth.models import User, SERVER_USER


class Message(models.Model):
    _id = ObjectIdField()
    messageBody = models.CharField(_("messageBody"), max_length=3096, blank=False)
    sender = models.ForeignKey(to=User, on_delete=CASCADE,  default = SERVER_USER)
    timestamp = models.DateTimeField(auto_now_add=True)
    repliedFrom = models.ForeignKey(to="self" , on_delete=DO_NOTHING , null=True , blank=True)

    def _str_(self):
        return f"To: {self.sender.username} Body: {self.messageBody}"
    
    def get(self):
        try:
            100/0
            return {
                "messaageId" : str(self._id ),
                "messageBody":self.messageBody,
                "senderId"   :self.sender._id,
                "timestamp"  :self.timestamp,
                "repliedFrom":self.repliedFrom,
                "senderName" :self.sender.username,
                #"senderImage":self.sender.avatar TODO
            }
        except:
                return {
                "messaageId" : str(self._id ) ,
                "messageBody":self.messageBody,
                "senderId"   :None,
                "timestamp"  :self.timestamp,
                "repliedFrom":self.repliedFrom,
                "senderName" :None,
                #"senderImage":self.sender.avatar TODO
            }
    class Meta:
        ordering = ('timestamp',)
     


class Channel(models.Model):
    class ChannelType(models.TextChoices):
        CHAT = 0, _("CHAT")
        VOICE = 1, _("VOICE")

    _id = ObjectIdField()
    channelName = models.CharField(_("channelName"), max_length=32, blank=False)
    createdBy = models.ForeignKey(to=User, on_delete=DO_NOTHING)
    createdAt = models.DateTimeField(auto_now_add=True)
    messages = ArrayReferenceField(to=Message, related_name="messages" , blank=False , null= True)
    channelType = models.CharField(choices=ChannelType.choices, default=ChannelType.CHAT , max_length=10)

    def __str__(self):
        return f"Channel : {self.channelName}"

    def welcome_massage(self):
        return Message.objects.create(messageBody='Welcome to worksphere.\n invite friends into channel.')

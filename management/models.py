from django.db import models
from django.db.models import CASCADE, DO_NOTHING
from djongo.models import ObjectIdField, ArrayReferenceField
from django.utils.translation import gettext_lazy as _

from userAuth.models import User
from chat.models import Channel


class Company(models.Model):
    _id = ObjectIdField()
    companyName = models.CharField(_("companyName"), max_length=32)
    companyOwner = models.ForeignKey(to=User, on_delete=CASCADE)
    users = ArrayReferenceField(to=User, related_name="users", on_delete=CASCADE)
    channels = ArrayReferenceField(to=Channel, related_name="channels", on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


class CompanyUser(models.Model):
    _id = ObjectIdField()
    company = models.ForeignKey(to=Company, on_delete=CASCADE)
    roles = ArrayReferenceField(to=Role)


class Task(models.Model):
    _id = ObjectIdField()
    taskName = models.CharField(_("taskName"), max_length=128)
    taskDescription = models.CharField(_("taskDescription"), max_length=1024)
    createdBy = models.ForeignKey(to=User, related_name="createdBy", on_delete=DO_NOTHING)
    assignedTo = ArrayReferenceField(to=User, related_name="assignedTo", on_delete=DO_NOTHING)
    # additionlFields=Obj TODO: To be Added

from django.utils.translation import gettext_lazy as _
from django.db.models import CASCADE, DO_NOTHING
from djongo.models import DjongoManager, ArrayField

from management.managers import CompanyManager
from userAuth.models import User
from chat.models import Channel

from .abstract_models import *


class Company(models.Model):
    _id = ObjectIdField()
    companyName = models.CharField(_("companyName"), max_length=32)
    companyOwner = models.ForeignKey(to=User, on_delete=CASCADE)
    users = ArrayReferenceField(to=CompanyUser, related_name="users", on_delete=CASCADE)
    channels = ArrayReferenceField(to=Channel, related_name="channels", on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    roles = ArrayReferenceField(to=Role, related_name="roles", on_delete=CASCADE)

    manager = CompanyManager()

    def __str__(self):
        return str(self._id)


class Task(models.Model):
    _id = ObjectIdField()
    taskName = models.CharField(_("taskName"), max_length=128)
    taskDescription = models.CharField(_("taskDescription"), max_length=1024)
    createdBy = models.ForeignKey(to=User, related_name="createdBy", on_delete=DO_NOTHING)
    assignedTo = ArrayReferenceField(to=User, related_name="assignedTo", on_delete=DO_NOTHING)
    additional_fields = ArrayField(model_container=TaskCustomFields)

    manager = DjongoManager()

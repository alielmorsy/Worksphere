from django.db import models
from django.db.models import CASCADE
from djongo.models import ObjectIdField, ArrayReferenceField, JSONField, DjongoManager
from userAuth.auth import User


class Role(models.Model):
    _id = ObjectIdField()
    role_name = models.CharField(max_length=32)
    role_color = models.IntegerField()
    permissions = models.IntegerField()


class CompanyUser(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(to=User, on_delete=CASCADE)
    roles = ArrayReferenceField(to=Role, on_delete=CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    company_note = models.CharField(max_length=3096)  # Simple string that work as a note for the company.

    models = DjongoManager()


class TaskCustomFields(models.Model):
    class FieldType(models.IntegerChoices):
        TEXT_BOX = 1
        MULTIPLE_SELECTION = 2
        CHECK_BOX = 3

    _id = ObjectIdField()
    field_name = models.CharField(max_length=32)
    field_type = models.IntegerField(choices=FieldType, default=FieldType.TEXT_BOX)
    value = models.CharField()
    additional_info = JSONField()  # Should contain anything needs to be added.

    class Meta:
        abstract = True

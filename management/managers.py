from django.db import models
from django.db.models.manager import BaseManager

from djongo.models import DjongoManager

from chat.models import Channel
from management.abstract_models import Role, CompanyUser
from management.permission_utils import DefaultPermissions


class CompanyManager(models.Manager):

    def create(self, **kwargs):
        """
        Custom create function that create Company object, add new role to that company,
        and assign the owner to that role
        """
        company = super().create(**kwargs)
        user = kwargs["companyOwner"]
        general_channel = Channel.objects.create(channelName="general", channelType=Channel.ChannelType.CHAT,
                                                 createdBy=user)
        company.channels.add(general_channel)
        admin_role = Role(role_name="Admin", role_color=0xFFD700, permissions=DefaultPermissions.ADMIN)  # Golden Color
        admin_role.save()
        company.roles.add(admin_role)

        admin_company_user = CompanyUser(user=user)
        admin_company_user.roles.add(admin_role)
        admin_company_user.save()

        company.users.add(admin_company_user)
        company.save()

        return company

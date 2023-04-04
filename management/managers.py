from djongo.models import DjongoManager

from chat.models import Channel
from management.abstract_models import Role, CompanyUser
from management.permission_utils import DefaultPermissions


class CompanyManager(DjongoManager):

    def create(self, **kwargs):
        """
        Custom create function that create Company object, add new role to that company,
        and assign the owner to that role
        """
        if "owner" not in kwargs:
            raise RuntimeWarning("Owner is not exists while creating the company")
        user = kwargs["companyOwner"]
        general_channel = Channel.objects.create(channelName="general", channelType=Channel.ChannelType.CHAT,
                                                 createdBy=user)
        self.channels.add(general_channel)
        admin_role = Role(role_name="Admin", role_color=0xFFD700, permissions=DefaultPermissions.ADMIN)
        self.roles.add(admin_role)
        admin_company_user = CompanyUser(user=user)
        admin_company_user.roles.add(admin_role)
        self.users.add(admin_company_user)

        company = super().create(**kwargs)
        return company

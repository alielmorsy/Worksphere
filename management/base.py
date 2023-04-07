from bson import ObjectId

from management.permission_utils import DefaultPermissions


class AuthorizedCompanyBase:
    """
    Class should be inherited in every API request that includes company checks.
    It contains main function get_company_id which initial implementation which grabs the company_id from
    post body. and return it to be used somewhere else in the code.
    """

    default_permissions = DefaultPermissions.REGULAR_USER

    def get_company_id(self, request):
        data = request.data
        if "company_id" not in data:
            raise RuntimeError("Bad Request")
        return ObjectId(data["companyId"])

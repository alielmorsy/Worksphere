from Worksphere.BaseService import BaseService
from ..models import User


class LoginService(BaseService):
    def login(self, userName, password):
        result = User.objects.filter(username=userName)
        if len(result) == 0:
            raise LoginError("Invalid User Name or Password")
        user = result[0]
        if not user.check_password(password):
            raise LoginError("Invalid User Name or Password")

        return user


class LoginError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

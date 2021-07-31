from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from my_auth.models import User


class UserLogic:
    @staticmethod
    def update_user(user: "User", data: dict) -> None:
        user.update(**data)

"""
api.permissions: the typed services of an authentication provider (permissions_app).
"""

from abc import ABC, abstractmethod

from ycappuccino.api.core_base import YCappuccinoComponent
from ycappuccino.api.decorators import rpc_method


class ILoginService(YCappuccinoComponent, ABC):
    """exchanges credentials for a token"""

    @rpc_method(summary="exchange a login and a password for a token", secure=False)
    @abstractmethod
    async def login(self, login: str, password: str) -> str:
        """the token of the account of this login; NotFound/InvalidRequest when the credentials are wrong"""

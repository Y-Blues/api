"""
api.http_server: authentication port used by HTTP adapters (http_server, and later others).
"""

from abc import ABC, abstractmethod

from ycappuccino.api.core_base import YCappuccinoComponent


class IAuthentication(YCappuccinoComponent, ABC):
    """decodes the subject of an HTTP request; several may be active, tried in turn"""

    @abstractmethod
    async def authenticate(self, headers: dict, method: str, path: str, body: bytes) -> dict | None:
        """subject decoded from the request, or None when this provider does not recognize it.
        method/path/body let a provider verify a signature covering the whole request (see remote's
        peer HMAC authentication); a header-only provider (a JWT) simply ignores them."""

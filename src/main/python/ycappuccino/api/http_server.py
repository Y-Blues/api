"""
api.http_server: authentication port used by HTTP adapters (http_server, and later others).
"""

from abc import ABC, abstractmethod
from typing import Optional

from ycappuccino.api.core_base import YCappuccinoComponent


class IAuthentication(YCappuccinoComponent, ABC):
    """decodes the subject of an HTTP request from its headers"""

    @abstractmethod
    async def authenticate(self, headers: dict) -> Optional[dict]:
        """subject decoded from the headers, or None when absent or invalid"""

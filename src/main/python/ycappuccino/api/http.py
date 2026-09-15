"""
api.http: contract of a component that answers HTTP requests, without any dependency on Pelix.

HttpRequest and HttpResponse are plain dataclasses so this module stays importable outside the
framework (e.g. the pyscript client). ycappuccino.core translates them to and from the real
Pelix HTTP servlet API for a component that implements IHttpServlet.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ycappuccino.api.core_base import YCappuccinoComponent


@dataclass
class HttpRequest:
    """HTTP request received by a servlet"""
    method: str
    path: str
    prefix: str
    sub_path: str
    query: dict
    headers: dict
    body: bytes = b""


@dataclass
class HttpResponse:
    """HTTP response returned by a servlet"""
    status: int
    body: bytes = b""
    content_type: str = "application/json"
    headers: dict = field(default_factory=dict)


class IHttpServlet(YCappuccinoComponent, ABC):
    """component answering the HTTP requests received under its path property"""

    @abstractmethod
    async def handle(self, request: HttpRequest) -> HttpResponse:
        """process the request and return the response"""

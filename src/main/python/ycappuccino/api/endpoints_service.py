"""
api.endpoints_service: calling a named service, independent of any transport.

Reuses endpoints_storage's error family (NotAuthenticated, Forbidden, NotFound, InvalidRequest)
and its IAuthorization port: services and items share the same authorization mechanism.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from ycappuccino.api.core_base import YCappuccinoComponent
from ycappuccino.api.decorators import rpc_method
from ycappuccino.api.endpoints_storage import NotFound

# action checked by IAuthorization for a secure service
CALL = "call"


@dataclass
class ServiceResult:
    """result of a service call"""
    body: Any
    headers: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ServiceRoute:
    """a request answered by a service, documented in the API descriptions (swagger)"""
    method: str
    # extra path after the service name; "{name}" segments are path parameters
    path: str = ""
    summary: str = ""
    # parameter name -> type, and the return type, of the method answering the request
    params: dict = field(default_factory=dict)
    return_type: type | None = None


class IExposedService(YCappuccinoComponent, ABC):
    """a named action, published under its name.

    A service answers its requests either through its @rpc_method methods (IServiceEndpoint routes a
    request to the one whose HTTP method and path template match), or by overriding call() to handle
    every request itself; an overridden call() takes precedence."""

    name: str = ""
    secure: bool = True
    # ServiceRoute instances describing the requests the service answers; empty: undocumented
    routes: tuple = ()

    async def call(
        self, method: str, extra_path: list, params: dict, body: Any, subject: Optional[dict]
    ) -> ServiceResult:
        """handle the request; raise NotFound (endpoints_storage) for an unsupported method/extra_path"""
        raise NotFound(f"service {self.name} does not handle {method} requests itself")


class IServiceEndpoint(YCappuccinoComponent, ABC):
    """finds a service by name and dispatches to it, applying its authorization"""

    @rpc_method(summary="call a named service", secure=False)
    @abstractmethod
    async def call(
        self, name: str, method: str, extra_path: list, params: dict, body: Any, subject: Optional[dict]
    ) -> ServiceResult:
        """NotFound if no service has this name; NotAuthenticated/Forbidden if it is secure and refused"""

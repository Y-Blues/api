"""
Core api description

@author: apisu
"""

import logging
import uuid
from abc import ABC
from typing import Any

from ycappuccino.api.core.base import YCappuccinoComponent, YCappuccinoComponentBind
from ycappuccino.api.proxy.api import YCappuccinoRemote


class IActivityLogger(YCappuccinoComponent, logging.Logger, ABC):
    """Activity logger of the application. admit a property name that identified the logger"""

    def __init__(self):
        super(IActivityLogger, self).__init__(
            "activity-{}".format(uuid.uuid4().__str__())
        )


class IConfiguration(YCappuccinoComponent, ABC):
    """interface of configuration service"""

    def __init__(self):
        super(YCappuccinoComponent, self).__init__()

    def get(self, a_key: str, a_default: str) -> Any:
        raise NotImplementedError


class IListComponent(YCappuccinoComponentBind, ABC):
    """interface of YCappuccino component that list of YCappuccino component"""

    def call(self, a_comp_name, a_method):
        raise NotImplementedError


class IServerProxy:
    """interface of the service endpoint that list proxy"""


class IService(YCappuccinoRemote):
    """interface that describe a service"""

    def __init__(self):
        super().__init__()

    def is_sercure(self) -> bool:
        return True

    def has_post(self) -> bool:
        return True

    def has_put(self) -> bool:
        return False

    def has_get(self) -> bool:
        return False

    def has_delete(self) -> bool:
        return False

    def has_root_path(self) -> bool:
        return True

    def get_name(self) -> str:
        pass

    def get_extra_path(self) -> dict:
        """return the list of extra path that are manage by service"""
        return {"post": [], "get": [], "put": [], "delete": []}

    def post(self, a_header, a_url_path, a_body):
        pass

    def put(self, a_header, a_url_path, a_body):
        pass

    def get(self, a_header, a_url_path):
        pass

    def delete(self, a_header, a_url_path):
        pass

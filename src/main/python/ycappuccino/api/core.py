"""
Core api description

@author: apisu
"""

import logging
import uuid
from abc import ABC
from typing import Any
from ycappuccino.api.core_base import YCappuccinoComponent


class IActivityLogger(YCappuccinoComponent, logging.Logger, ABC):
    """Activity logger of the application. admit a property name that identified the logger"""

    def __init__(self) -> None:
        super(IActivityLogger, self).__init__(
            "activity-{}".format(uuid.uuid4().__str__())
        )


class IConfiguration(YCappuccinoComponent, ABC):
    """interface of configuration service"""

    def __init__(self) -> None:
        super(YCappuccinoComponent, self).__init__()

    def get(self, a_key: str, a_default: str) -> Any:
        raise NotImplementedError


class IServerProxy:
    """interface of the service endpoint that list proxy"""

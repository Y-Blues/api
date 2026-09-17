from typing import Any

from pelix.ipopo.decorators import Property  # type: ignore

from ycappuccino.api.core_base import CFQCN


class IComponentServiceList(object):
    """interface of YCappuccino component"""

    name = CFQCN.build("IComponentServiceList")

    def __init__(self) -> None:
        """abstract constructor"""
        pass


@Property("_model", "model", None)
class IComponentServiceFactory(object):
    """interface of YCappuccino component"""

    name = CFQCN.build("IComponentServiceFactory")

    def __init__(self) -> None:
        """abstract constructor"""
        self._model = None


class IHttp(IComponentServiceFactory):
    """interface of YCappuccino component"""

    name = CFQCN.build("IHttp")

    def __init__(self) -> None:
        """abstract constructor"""
        super(IComponentServiceFactory, self).__init__()

    def get(self, a_header: dict, a_url: str) -> Any:
        """abstract constructor"""
        pass

    def post(self, a_header: dict, a_url: str, body: Any) -> Any:
        """abstract constructor"""
        pass

    def delete(self, a_header: dict, a_url: str) -> Any:
        """abstract constructor"""
        pass

    def put(self, a_header: dict, a_url: str, body: Any) -> Any:
        """abstract constructor"""
        pass


class IMail(IComponentServiceFactory):
    """interface of YCappuccino component"""

    name = CFQCN.build("IMail")

    def __init__(self) -> None:
        """abstract constructor"""
        super(IComponentServiceFactory, self).__init__()

    def send(self, a_mail: Any) -> Any:
        """abstract constructor"""
        pass


class IMqtt(IComponentServiceFactory):
    """interface of YCappuccino component"""

    name = CFQCN.build("IMqtt")

    def __init__(self) -> None:
        """abstract constructor"""
        super(IComponentServiceFactory, self).__init__()

    # paho-mqtt callback conventions -- args come from the mqtt client library, not imported here
    def on_connect(client: Any, userdata: Any, flags: Any, rc: Any) -> None:
        pass

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client: Any, userdata: Any, msg: Any) -> None:
        pass

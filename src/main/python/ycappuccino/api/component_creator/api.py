from pelix.ipopo.decorators import Property

from ycappuccino.api.core.base import CFQCN


class IComponentServiceList(object):
    """interface of YCappuccino component"""

    name = CFQCN.build("IComponentServiceList")

    def __init__(self):
        """abstract constructor"""
        pass


@Property("_model", "model", None)
class IComponentServiceFactory(object):
    """interface of YCappuccino component"""

    name = CFQCN.build("IComponentServiceFactory")

    def __init__(self):
        """abstract constructor"""
        self._model = None

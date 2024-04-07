# app="all"
from ycappuccino.api.core.base import CFQCN
from ycappuccino.api.proxy.api import YCappuccinoRemote


class IClobReplaceService(YCappuccinoRemote):
    """interface of YCappuccino component"""

    name = CFQCN.build("IClobReplaceService")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()


class IHost(YCappuccinoRemote):
    """interface of that represent a path location for static file deliver by the server"""

    name = CFQCN.build("IHost")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()


class IHostFactory(YCappuccinoRemote):
    """interface of that create IHost regarding host models stored"""

    name = CFQCN.build("IHostFactory")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

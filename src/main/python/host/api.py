# app="all"
from src.main.python.proxy import YCappuccinoRemote, CFQCN


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

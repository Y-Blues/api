# app="all"

from ycappuccino.api.core.base import CFQCN
from ycappuccino.api.proxy.api import YCappuccinoRemote
from ycappuccino.api.storage.api import IRightSubject


class IRemoteServer(IRightSubject):
    """interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component
    """

    name = CFQCN.build("IRemoteServer")

    def __init__(self):
        """abstract constructor"""
        super(IRightSubject, self).__init__()


class IRemoteComponentProxy(object):
    """interface of YCappuccino component"""

    name = CFQCN.build("IRemoteComponentProxy")

    def __init__(self):
        """abstract constructor"""
        pass


class IRemoteClient(object):
    """interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component
    """

    name = CFQCN.build("IRemoteClient")

    def __init__(self):
        """abstract constructor"""
        pass


class IRemoteComponentProxyFactory(object):
    name = CFQCN.build("IRemoteComponentProxyFactory")

    def __init__(self):
        """abstract constructor"""
        pass


class IRemoteClientFactory(object):
    """interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component
    """

    name = CFQCN.build("IRemoteClientFactory")

    def __init__(self):
        """abstract constructor"""
        pass

    def create_remote_client(self, a_remote_server):
        pass

    def remove_remote_client(self, a_remote_server):
        pass


class IRemoteStorage(object):
    """interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component
    """

    name = CFQCN.build("IRemoteStorage")

    def __init__(self):
        """abstract constructor"""
        super().__init__()


class IRemoteStorageFactory(object):
    """interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component
    """

    name = CFQCN.build("IRemoteStorageFactory")

    def __init__(self):
        """abstract constructor"""
        super().__init__()


class IRemoteManager(object):
    """interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component
    """

    name = CFQCN.build("IRemoteManager")

    def __init__(self):
        """abstract constructor"""
        super().__init__()

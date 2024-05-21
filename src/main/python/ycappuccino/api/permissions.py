# app="all"
from ycappuccino.api.core_base import CFQCN
from ycappuccino.api.proxy import YCappuccinoRemote


class ILoginService(YCappuccinoRemote):
    """interface of Login Service"""

    name = CFQCN.build("ILoginService")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()


class ITenantTrigger(YCappuccinoRemote):
    """interface of multi tenant"""

    name = CFQCN.build("ITenantTrigger")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

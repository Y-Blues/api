# app="all"
from ycappuccino.api.core.base import CFQCN
from ycappuccino.api.proxy.api import YCappuccinoRemote


class IScheduler(IService):
    """interface of a scheduler service"""

    name = CFQCN.build("IScheduler")

    def __init__(self):
        """abstract constructor"""
        super(IService, self).__init__()

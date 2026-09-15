# app="all"
from ycappuccino.api.core import IService
from ycappuccino.api.core_base import CFQCN


class IScheduler(IService):
    """interface of a scheduler service"""

    name = CFQCN.build("IScheduler")

    def __init__(self):
        """abstract constructor"""
        super(IService, self).__init__()

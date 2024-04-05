#app="all"
from ycappuccino_api.proxy.api import CFQCN
from ycappuccino_api.core.api import IService


class IScheduler(IService):
    """ interface of a scheduler service"""
    name = CFQCN.build("IScheduler")

    def __init__(self):
        """ abstract constructor """
        super(IService,self).__init__()


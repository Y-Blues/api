#app="all"
from ycappuccino_api.core.api import CFQCN


class ILoginService(object):
    """ interface of Login Service """
    name = CFQCN.build("ILoginService")

    def __init__(self):
        """ abstract constructor """
        pass


class ITenantTrigger(object):
    """ interface of multi tenant """
    name = CFQCN.build("ITenantTrigger")

    def __init__(self):
        """ abstract constructor """
        pass
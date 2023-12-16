#app="all"
from ycappuccino_api.core.api import CFQCN




class IClobReplaceService(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IClobReplaceService")

    def __init__(self):
        """ abstract constructor """
        pass


class IHost(object):
    """ interface of that represent a path location for static file deliver by the server """
    name = CFQCN.build("IHost")

    def __init__(self):
        """ abstract constructor """
        pass

class IHostFactory(object):
    """ interface of that create IHost regarding host models stored"""
    name = CFQCN.build("IHostFactory")

    def __init__(self):
        """ abstract constructor """
        pass

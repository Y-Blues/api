#app="all"
from ycappuccino_api.core.api import CFQCN


class IScriptInterpreter(object):
    """ interface of YCappuccino component that interprete javascript """
    name = CFQCN.build("IScriptInterpreter")

    def __init__(self):
        """ abstract constructor """
        pass


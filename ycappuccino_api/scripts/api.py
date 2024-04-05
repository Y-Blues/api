#app="all"
from ycappuccino_api.proxy.api import CFQCN
from ycappuccino_api.proxy.api import YCappuccinoRemote


class IScriptInterpreter(YCappuccinoRemote):
    """ interface of YCappuccino component that interprete javascript """
    name = CFQCN.build("IScriptInterpreter")

    def __init__(self):
        """ abstract constructor """
        super(YCappuccinoRemote,self).__init__()


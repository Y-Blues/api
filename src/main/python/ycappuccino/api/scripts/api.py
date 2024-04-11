# app="all"
from ycappuccino.api.core.base import CFQCN
from ycappuccino.api.proxy.api import YCappuccinoRemote


class IScriptInterpreter(YCappuccinoRemote):
    """interface of YCappuccino component that interprete javascript"""

    name = CFQCN.build("IScriptInterpreter")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

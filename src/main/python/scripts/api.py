# app="all"
from src.main.python.proxy import CFQCN
from src.main.python.proxy import YCappuccinoRemote


class IScriptInterpreter(YCappuccinoRemote):
    """interface of YCappuccino component that interprete javascript"""

    name = CFQCN.build("IScriptInterpreter")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

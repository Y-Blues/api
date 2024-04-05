from __future__ import annotations

import abc
import typing as t
import logging
from pelix.ipopo.decorators import Validate, Invalidate, BindField, UnbindField


class CFQCN(object):
    """
    CFQCN class : Ful Qualified Class Name
    """

    @staticmethod
    def build(a_class_name: str):
        w_fqcn = ".".join(["ycappuccino_api", a_class_name])
        log = logging.getLogger(__name__)
        log.info("FQCN '{0}' ...".format(w_fqcn))
        return w_fqcn


class YCappuccinoComponent(abc.ABC):

    @abc.abstractmethod
    async def start(self):
        """start statement for this component"""
        ...

    @abc.abstractmethod
    async def stop(self):
        """stop statement for this component"""

        ...


class YCappuccinoComponentBind(YCappuccinoComponent):

    def __init__(self):
        self._bind_field = []

    @abc.abstractmethod
    async def bind(self, a_service: t.Any):
        """bind statement for this component"""
        ...

    @abc.abstractmethod
    async def un_bind(self, a_service: t.Any):
        """unbind statement for this component"""
        ...


class DefaultMixin:
    spec_filter: t.Union[str, YCappuccinoComponent] = "main"


class _YCappuccinoType:
    def __init__(self, value):
        self.value = value


def YCappuccinoType(base_type: type, spec_filter: t.Any = None) -> type:
    class YCappuccinoTypeDefault(_YCappuccinoType, base_type, DefaultMixin):
        @classmethod
        def set_default(cls, value1: type, value2: str):
            cls.type = value1
            cls.spec_filter = value2

    YCappuccinoTypeDefault.set_default(base_type, spec_filter)

    return YCappuccinoTypeDefault

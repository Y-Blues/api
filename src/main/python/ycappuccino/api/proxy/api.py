import types, json
from pprint import pformat


from ycappuccino.api.core.base import CFQCN


def get_class(kls):
    parts = kls.split(".")
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


class ProxyMethodWrapper:
    """
    Wrapper object for a method to be called.
    """

    def __init__(self, obj, func, name):
        self.obj, self.func, self.name = obj, func, name
        assert obj is not None
        assert func is not None
        assert name is not None

    def __call__(self, *args, **kwds):
        return self.obj._method_call(self.name, self.func, *args, **kwds)


class Proxy(object):

    def __init__(self):
        self._objname: str = ""
        self._obj: any = None

    def __getattribute__(self, name: str) -> types.MethodType:
        """
        Return a proxy wrapper object if this is a method call.
        """
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        else:
            if self._obj is not None:
                att = getattr(self._obj, name)
            else:
                att = object.__getattribute__(self, name)

            if type(att) is types.MethodType:
                return ProxyMethodWrapper(self, att, name)
            else:
                return att

    def __setitem__(self, key: str, value: any) -> None:
        """
        Delegate [] syntax.
        """
        name = "__setitem__"
        if self._obj is not None:
            att = getattr(self._obj, name)
        else:
            att = object.__getattribute__(self, name)
        p_meth = ProxyMethodWrapper(self, att, name)
        p_meth(key, value)

    def _call_str(self, name, *args, **kwds):
        """
        Returns a printable version of the call.
        This can be used for tracing.
        """
        pargs = [pformat(x) for x in args]
        for k, v in kwds.iteritems():
            pargs.append("%s=%s" % (k, pformat(v)))
        if self._objname is not None:
            return "%s.%s(%s)" % (self._objname, name, ", ".join(pargs))
        else:
            return "%s.%s(%s)" % (self.__str__(), name, ", ".join(pargs))

    def _method_call(self, name, func, *args, **kwds):
        """
        This method gets called before a method is called.
        """
        # pre-call hook for all calls.
        try:
            prefunc = getattr(self, "_pre")
        except AttributeError:
            pass
        else:
            prefunc(name, *args, **kwds)

        # pre-call hook for specific method.
        try:
            prefunc = getattr(self, "_pre_%s" % name)
        except AttributeError:
            pass
        else:
            prefunc(*args, **kwds)

        # get real method to call and call it
        rval = func(*args, **kwds)

        # post-call hook for specific method.
        try:
            postfunc = getattr(self, "_post_%s" % name)
        except AttributeError:
            pass
        else:
            postfunc(*args, **kwds)

        # post-call hook for all calls.
        try:
            postfunc = getattr(self, "_post")
        except AttributeError:
            pass
        else:
            postfunc(name, *args, **kwds)

        return rval


class YCappuccinoRemote(object):
    """interface of YCappuccino component"""

    name = CFQCN.build("YCappuccinoRemote")

    def __init__(self):
        """abstract constructor"""
        self._specifications: list = []
        self._id: str = ""
        self._component_properties: dict = {}
        self._remote_server_id: str = ""
        self._methods: list = dir(self)

    def get_component_properties_id(self) -> str:
        prop = self._component_properties.copy()
        prop["specifications"] = self._specifications
        prop["remote_server_id"] = self._remote_server_id
        prop["methods"] = self._methods

        return json.dumps(prop)

    def get_specifications(self) -> list:
        return self._specifications

    def set_specifications(self, a_specifications: list) -> None:
        self._specifications = a_specifications

    def set_component_properties(self, a_component_properties: dict) -> None:
        self._component_properties = a_component_properties.copy()
        w_object_class = self._component_properties["objectClass"]
        self._specifications = []
        for w_class in w_object_class:
            self._specifications.append(w_class)

    def set_component_id_remote(self, a_component_id_remote: str) -> None:
        self._remote_server_id = a_component_id_remote

    def id(self) -> str:
        return self._id

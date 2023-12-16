import types
from pprint import pformat
from pelix.ipopo.decorators import Property

from ycappuccino_api.core.api import YCappuccino, CFQCN


class ProxyMethodWrapper:
    """
    Wrapper object for a method to be called.
    """

    def __init__( self, obj, func, name ):
        self.obj, self.func, self.name = obj, func, name
        assert obj is not None
        assert func is not None
        assert name is not None

    def __call__( self, *args, **kwds ):
        return self.obj._method_call(self.name, self.func, *args, **kwds)

class Proxy(object):

    def __init__(self):
        self._objname = None
        self._obj = None

    def __getattribute__(self, name):
        """
        Return a proxy wrapper object if this is a method call.
        """
        if name.startswith('_'):
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

    def __setitem__(self, key, value):
        """
        Delegate [] syntax.
        """
        name = '__setitem__'
        if self._obj is not None:
            att = getattr(self._obj, name)
        else:
            att = object.__getattribute__(self, name)
        pmeth = ProxyMethodWrapper(self, att, name)
        pmeth(key, value)

    def _call_str(self, name, *args, **kwds):
        """
        Returns a printable version of the call.
        This can be used for tracing.
        """
        pargs = [pformat(x) for x in args]
        for k, v in kwds.iteritems():
            pargs.append('%s=%s' % (k, pformat(v)))
        if self._objname is not None:
            return '%s.%s(%s)' % (self._objname, name, ', '.join(pargs))
        else:
            return '%s.%s(%s)' % (self.__str__(), name, ', '.join(pargs))

    def _method_call(self, name, func, *args, **kwds):
        """
        This method gets called before a method is called.
        """
        # pre-call hook for all calls.
        try:
            prefunc = getattr(self, '_pre')
        except AttributeError:
            pass
        else:
            prefunc(name, *args, **kwds)

        # pre-call hook for specific method.
        try:
            prefunc = getattr(self, '_pre_%s' % name)
        except AttributeError:
            pass
        else:
            prefunc(*args, **kwds)

        # get real method to call and call it
        rval = func(*args, **kwds)

        # post-call hook for specific method.
        try:
            postfunc = getattr(self, '_post_%s' % name)
        except AttributeError:
            pass
        else:
            postfunc(*args, **kwds)

        # post-call hook for all calls.
        try:
            postfunc = getattr(self, '_post')
        except AttributeError:
            pass
        else:
            postfunc(name, *args, **kwds)

        return rval

@Property("_obj","object",None)
@Property("_objname","object_name",None)
class YCappuccinoProxy(YCappuccino, Proxy):
    """ interface of YCappuccino component """
    name = CFQCN.build("YCappuccinoProxy")

    def __init__(self):
        """ abstract constructor """
        super().__init__()

import unittest

from ycappuccino.api.proxy import Proxy


class Greeter(object):
    value = 42

    def hello(self, name, punctuation="!"):
        return f"hello {name}{punctuation}"


class TracingProxy(Proxy):

    def __init__(self, obj):
        super().__init__()
        self._obj = obj
        self._objname = "greeter"
        self._trace = []

    def _pre(self, name, *args, **kwds):
        self._trace.append(("pre", name))

    def _post(self, name, *args, **kwds):
        self._trace.append(("post", name))


class TestProxy(unittest.TestCase):

    def setUp(self):
        self.proxy = TracingProxy(Greeter())

    def test_method_calls_are_delegated(self):
        self.assertEqual(self.proxy.hello("bob", punctuation="?"), "hello bob?")

    def test_attributes_are_delegated(self):
        self.assertEqual(self.proxy.value, 42)

    def test_hooks_surround_the_call(self):
        self.proxy.hello("bob")

        self.assertEqual(self.proxy._trace, [("pre", "hello"), ("post", "hello")])

    def test_call_str_renders_positional_and_keyword_arguments(self):
        self.assertEqual(
            self.proxy._call_str("hello", "bob", punctuation="?"),
            "greeter.hello('bob', punctuation='?')",
        )


if __name__ == "__main__":
    unittest.main()

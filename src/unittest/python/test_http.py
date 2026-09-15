import dataclasses
import inspect
import unittest

from ycappuccino.api.core_base import YCappuccinoComponent
from ycappuccino.api.http import HttpRequest, HttpResponse, IHttpServlet


class TestHttpRequest(unittest.TestCase):

    def test_is_a_plain_dataclass(self):
        self.assertTrue(dataclasses.is_dataclass(HttpRequest))
        request = HttpRequest(
            method="GET", path="/api/books", prefix="/api", sub_path="/books",
            query={"limit": "5"}, headers={"authorization": "Bearer x"},
        )
        self.assertEqual(request.body, b"")

    def test_no_pelix_import(self):
        import ycappuccino.api.http as module
        self.assertNotIn("pelix", module.__name__)
        for name, value in vars(module).items():
            if inspect.ismodule(value):
                self.assertFalse(value.__name__.startswith("pelix"), name)


class TestHttpResponse(unittest.TestCase):

    def test_defaults(self):
        response = HttpResponse(status=200)
        self.assertEqual(response.body, b"")
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.headers, {})

    def test_headers_default_is_not_shared(self):
        HttpResponse(status=200).headers["x"] = "1"
        self.assertEqual(HttpResponse(status=200).headers, {})


class TestIHttpServlet(unittest.TestCase):

    def test_is_abstract_component(self):
        self.assertTrue(issubclass(IHttpServlet, YCappuccinoComponent))
        self.assertTrue(inspect.isabstract(IHttpServlet))

    def test_handle_is_a_coroutine(self):
        self.assertTrue(inspect.iscoroutinefunction(IHttpServlet.handle))


if __name__ == "__main__":
    unittest.main()

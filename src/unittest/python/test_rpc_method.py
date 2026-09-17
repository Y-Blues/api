import abc
import inspect
import unittest

from ycappuccino.api.core_base import YCappuccinoComponent
from ycappuccino.api.decorators import get_rpc_methods, rpc_method
from ycappuccino.api.endpoints_service import IServiceEndpoint, ServiceRoute
from ycappuccino.api.endpoints_storage import ICrud, IDrafts, IItemCatalog
from ycappuccino.api.permissions import ILoginService


class IGreeter(YCappuccinoComponent, abc.ABC):

    @rpc_method(summary="say hello")
    @abc.abstractmethod
    async def greet(self, name: str, times: int = 1) -> str:
        """greets someone"""

    @abc.abstractmethod
    async def internal_only(self) -> None:
        """never public"""


class Greeter(IGreeter):

    async def greet(self, name: str, times: int = 1) -> str:
        return " ".join([f"hello {name}"] * times)

    async def internal_only(self) -> None:
        pass

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass


class TestRpcMethod(unittest.TestCase):

    def test_marks_the_function_with_its_typed_metadata(self):
        metadata = IGreeter.greet._ycappuccino_rpc_method

        self.assertEqual(metadata["method"], "POST")
        self.assertEqual(metadata["path"], "")
        self.assertEqual(metadata["summary"], "say hello")
        self.assertTrue(metadata["secure"])
        self.assertEqual(metadata["params"], {"name": str, "times": int})
        self.assertEqual(metadata["return_type"], str)

    def test_does_not_change_the_method_nor_its_abstractness(self):
        self.assertTrue(inspect.isabstract(IGreeter))
        self.assertTrue(inspect.iscoroutinefunction(IGreeter.greet))

    def test_rest_route_and_secure_flag_are_recorded(self):
        class IRunner(abc.ABC):
            @rpc_method(method="GET", path="/{id}/run", secure=False)
            async def run(self, id: str) -> dict:
                """runs"""

        metadata = IRunner.run._ycappuccino_rpc_method
        self.assertEqual((metadata["method"], metadata["path"], metadata["secure"]), ("GET", "/{id}/run", False))

    def test_get_rpc_methods_only_returns_marked_methods(self):
        self.assertEqual(set(get_rpc_methods(IGreeter)), {"greet"})

    def test_an_implementation_inherits_the_marks_of_its_interface(self):
        self.assertEqual(set(get_rpc_methods(Greeter)), {"greet"})


class TestPublicInterfaces(unittest.TestCase):
    """the api interfaces a framework client (a browser) may call through __remote_dispatch__"""

    def test_storage_use_cases_are_public_and_check_access_themselves(self):
        for interface, names in (
            (ICrud, {"get_one", "get_many", "create", "update", "delete", "delete_many"}),
            (IDrafts, {"get_one", "get_many", "save", "publish", "discard"}),
            (IItemCatalog, {"get_items", "get_item", "get_item_by_plural", "get_schema", "get_empty"}),
            (IServiceEndpoint, {"call"}),
        ):
            with self.subTest(interface=interface.__name__):
                methods = get_rpc_methods(interface)
                self.assertEqual(set(methods), names)
                self.assertTrue(all(not metadata["secure"] for metadata in methods.values()))

    def test_login_is_public_and_typed(self):
        methods = get_rpc_methods(ILoginService)

        self.assertEqual(set(methods), {"login"})
        self.assertFalse(methods["login"]["secure"])
        self.assertEqual(methods["login"]["params"], {"login": str, "password": str})
        self.assertEqual(methods["login"]["return_type"], str)


class TestServiceRoute(unittest.TestCase):

    def test_params_and_return_type_default_to_empty(self):
        route = ServiceRoute(method="POST")

        self.assertEqual((route.params, route.return_type), ({}, None))

    def test_params_and_return_type_can_be_given(self):
        route = ServiceRoute(method="POST", params={"id": str}, return_type=dict)

        self.assertEqual((route.params, route.return_type), ({"id": str}, dict))



class TestServiceRoutes(unittest.TestCase):

    def test_explicit_routes_win(self):
        from ycappuccino.api.endpoints_service import IExposedService, ServiceRoute, service_routes

        class Documented(IExposedService):
            routes = (ServiceRoute("POST", summary="documented by hand"),)

            async def start(self):
                pass

            async def stop(self):
                pass

            @rpc_method(method="GET")
            async def status(self) -> str:
                return "ok"

        self.assertEqual(service_routes(Documented()), (ServiceRoute("POST", summary="documented by hand"),))

    def test_rpc_methods_become_typed_routes_without_the_subject(self):
        from ycappuccino.api.endpoints_service import IExposedService, ServiceRoute, service_routes

        class Typed(IExposedService):
            async def start(self):
                pass

            async def stop(self):
                pass

            @rpc_method(method="POST", path="/{item_id}/execute", summary="run")
            async def execute(self, item_id: str, count: int, subject: dict | None) -> dict:
                return {}

            @rpc_method(method="GET")
            async def status(self) -> str:
                return "ok"

        self.assertEqual(
            service_routes(Typed()),
            (
                ServiceRoute("POST", "/{item_id}/execute", "run", {"item_id": str, "count": int}, dict),
                ServiceRoute("GET", "", "", {}, str),
            ),
        )


if __name__ == "__main__":
    unittest.main()

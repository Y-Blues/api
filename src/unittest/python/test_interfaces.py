import inspect
import unittest

import ycappuccino.api.storage as storage_api
from ycappuccino.api.component_creator import IHttp, IMail, IMqtt
from ycappuccino.api.core import IConfiguration
from ycappuccino.api.core_base import YCappuccinoComponent, YCappuccinoType
from ycappuccino.api.proxy import YCappuccinoRemote
from ycappuccino.api.storage import (
    IFileStore,
    IFilter,
    IItemManager,
    IManager,
    IStorage,
    ITrigger,
)


class TestRemoteInterfaces(unittest.TestCase):

    def test_component_properties_define_specifications(self):
        remote = YCappuccinoRemote()
        remote.set_component_properties({"objectClass": ["IHost", "IEndpoint"], "id": "m"})

        self.assertEqual(remote.get_specifications(), ["IHost", "IEndpoint"])


class TestStorageInterfaces(unittest.TestCase):

    def test_storage_interfaces_are_abstract_components(self):
        for klass in (IStorage, IItemManager, IManager, ITrigger, IFilter, IFileStore):
            with self.subTest(interface=klass.__name__):
                self.assertTrue(issubclass(klass, YCappuccinoComponent))
                self.assertTrue(inspect.isabstract(klass))

    def test_storage_operations_are_coroutines(self):
        operations = (
            (IStorage, ("get_one", "get_many", "up_sert", "delete", "count")),
            (IManager, ("get_one", "get_many", "up_sert", "up_sert_model", "delete", "delete_many", "count")),
            (ITrigger, ("execute",)),
            (IFilter, ("get_filter",)),
            (IFileStore, ("put", "get", "delete")),
        )
        for klass, methods in operations:
            for method in methods:
                with self.subTest(method=f"{klass.__name__}.{method}"):
                    self.assertTrue(inspect.iscoroutinefunction(getattr(klass, method)))

    def test_trigger_defaults_are_overridden_by_class_attributes(self):
        class Audit(ITrigger):
            item_id = "book"
            actions = ("upsert",)

            async def execute(self, action, item_id, model):
                pass

            async def start(self):
                pass

            async def stop(self):
                pass

        self.assertEqual((ITrigger.item_id, ITrigger.actions, ITrigger.post), ("", (), True))
        self.assertEqual((Audit().item_id, Audit().actions, Audit().post), ("book", ("upsert",), True))

    def test_legacy_storage_interfaces_are_removed(self):
        for name in ("IDefaultManager", "IUploadManager", "IOrganizationManager", "IStorageFactory"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(storage_api, name))


class TestComponentFactoryInterfaces(unittest.TestCase):

    def test_model_is_initialised(self):
        for klass in (IHttp, IMail, IMqtt):
            with self.subTest(interface=klass.__name__):
                self.assertIsNone(klass()._model)


class TestCoreBase(unittest.TestCase):

    def test_ycappuccino_type_keeps_type_and_filter(self):
        logger_type = YCappuccinoType(IConfiguration, "(name=main)")

        self.assertIs(logger_type.type, IConfiguration)
        self.assertEqual(logger_type.spec_filter, "(name=main)")
        self.assertTrue(issubclass(logger_type, IConfiguration))

    def test_interfaces_stay_abstract_until_start_and_stop_are_implemented(self):
        class Incomplete(IConfiguration):
            pass

        class Complete(IConfiguration):
            async def start(self):
                pass

            async def stop(self):
                pass

        with self.assertRaises(TypeError):
            Incomplete()
        self.assertIsInstance(Complete(), YCappuccinoComponent)


class TestEndpointsStorageInterfaces(unittest.TestCase):

    def test_interfaces_are_abstract_components(self):
        from ycappuccino.api.endpoints_storage import IAuthorization, ICrud, IDrafts, IItemCatalog

        for klass in (ICrud, IDrafts, IItemCatalog, IAuthorization):
            with self.subTest(interface=klass.__name__):
                self.assertTrue(issubclass(klass, YCappuccinoComponent))
                self.assertTrue(inspect.isabstract(klass))

    def test_operations_are_coroutines(self):
        from ycappuccino.api.endpoints_storage import IAuthorization, ICrud, IDrafts, IItemCatalog

        operations = (
            (ICrud, ("get_one", "get_many", "create", "update", "delete", "delete_many")),
            (IDrafts, ("get_one", "get_many", "save", "publish", "discard")),
            (IItemCatalog, ("get_items", "get_item", "get_item_by_plural", "get_schema", "get_empty")),
            (IAuthorization, ("is_authorized",)),
        )
        for klass, methods in operations:
            for method in methods:
                with self.subTest(method=f"{klass.__name__}.{method}"):
                    self.assertTrue(inspect.iscoroutinefunction(getattr(klass, method)))

    def test_errors_share_a_base_class(self):
        from ycappuccino.api.endpoints_storage import (
            CrudError,
            Forbidden,
            InvalidRequest,
            NotAuthenticated,
            NotFound,
        )

        for klass in (NotAuthenticated, Forbidden, NotFound, InvalidRequest):
            with self.subTest(error=klass.__name__):
                self.assertTrue(issubclass(klass, CrudError))
        self.assertTrue(issubclass(CrudError, Exception))
        self.assertFalse(issubclass(InvalidRequest, ValueError))

    def test_actions(self):
        from ycappuccino.api import endpoints_storage

        self.assertEqual(
            (endpoints_storage.READ, endpoints_storage.WRITE, endpoints_storage.DELETE, endpoints_storage.PRIVATE),
            ("read", "write", "delete", "private"),
        )


class TestHttpServerInterfaces(unittest.TestCase):

    def test_authentication_is_an_abstract_coroutine(self):
        from ycappuccino.api.http_server import IAuthentication

        self.assertTrue(issubclass(IAuthentication, YCappuccinoComponent))
        self.assertTrue(inspect.isabstract(IAuthentication))
        self.assertTrue(inspect.iscoroutinefunction(IAuthentication.authenticate))

    def test_authentication_sees_the_whole_request(self):
        from ycappuccino.api.http_server import IAuthentication

        parameters = list(inspect.signature(IAuthentication.authenticate).parameters)

        self.assertEqual(parameters, ["self", "headers", "method", "path", "body"])


class TestEndpointsServiceInterfaces(unittest.TestCase):

    def test_interfaces_are_abstract_components(self):
        from ycappuccino.api.endpoints_service import IExposedService, IServiceEndpoint

        for klass in (IExposedService, IServiceEndpoint):
            with self.subTest(interface=klass.__name__):
                self.assertTrue(issubclass(klass, YCappuccinoComponent))
                self.assertTrue(inspect.isabstract(klass))

    def test_call_is_a_coroutine(self):
        from ycappuccino.api.endpoints_service import IExposedService, IServiceEndpoint

        self.assertTrue(inspect.iscoroutinefunction(IExposedService.call))
        self.assertTrue(inspect.iscoroutinefunction(IServiceEndpoint.call))

    def test_exposed_service_defaults(self):
        from ycappuccino.api.endpoints_service import IExposedService

        self.assertEqual((IExposedService.name, IExposedService.secure), ("", True))

    def test_service_result_is_a_dataclass_with_independent_headers(self):
        from ycappuccino.api.endpoints_service import ServiceResult

        result = ServiceResult(body={"a": 1})
        result.headers["x"] = "1"

        self.assertEqual(result.body, {"a": 1})
        self.assertEqual(ServiceResult(body=None).headers, {})

    def test_call_action(self):
        from ycappuccino.api.endpoints_service import CALL

        self.assertEqual(CALL, "call")


if __name__ == "__main__":
    unittest.main()

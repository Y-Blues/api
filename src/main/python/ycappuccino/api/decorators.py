"""

list of decorator for declaring models in application in a ORM Ycappuccino mechanism
"""

import typing as t

# decorators to describe item and element to store in mongo if it's mongo element
import functools
import inspect


class YDict(object):

    def __init__(self, *a_tuple: t.Any) -> None:
        for t_ in a_tuple:
            if isinstance(t_, dict):
                for k, v in t_.items():
                    setattr(self, k, v)


def _class_name(klass: type) -> str:
    """registry key of a model class: classes with the same name in different modules stay distinct"""
    return f"{klass.__module__}.{klass.__qualname__}"


def _property_schema(name: str, type: str, **constraints: t.Any) -> dict:
    schema = {"type": type, "description": "{}".format(name)}
    for constraint, value in constraints.items():
        if value is not None:
            schema[constraint] = value
    return schema


def _register_property(item: dict, metadata: dict) -> None:
    item["schema"]["properties"][metadata["name"]] = dict(metadata["schema"])
    private_properties = item.setdefault("private_property", [])
    if metadata["private"] and metadata["name"] not in private_properties:
        private_properties.append(metadata["name"])


def _register_class_properties(klass: type, item: dict) -> None:
    """declare in the item the @Property setters of the class and of its parents"""
    for attribute_name in dir(klass):
        attribute = getattr(klass, attribute_name, None)
        metadata = getattr(attribute, "_ycappuccino_property", None)
        if metadata is not None:
            _register_property(item, metadata)


class Item(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(
        self,
        collection: str,
        name: str,
        plural: str,
        abstract: bool = False,
        module: str = "system",
        app: str = "ycappuccino_core",
        secure_read: bool = False,
        secure_write: bool = False,
        is_writable: bool = True,
        multipart: t.Any = None,
    ) -> None:
        self._meta_name = name
        self._meta_collection = collection
        self._meta_module = module
        self._item = {
            "id": name,
            "module": module,
            "abstract": abstract,
            "collection": collection,
            "plural": plural,
            "secureRead": secure_read,
            "secureWrite": secure_write,
            "isWritable": is_writable,
            "app": app,
            "multipart": multipart,
            "schema": {
                "$id": name,
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": name,
                "type": "object",
                "properties": {},
            },
            "empty": None,
        }

    def __call__(self, obj: type) -> type:
        self._super_class = (
            _class_name(obj.__bases__[0])
            if len(obj.__bases__) > 0 and obj.__bases__[0] is not YDict
            else None
        )
        self._class = _class_name(obj)
        self._item["father"] = self._super_class
        self._item["_class"] = self._class
        self._item["_class_obj"] = obj

        if self._class not in map_item_by_class:
            map_item_by_class[self._item["_class"]] = self._item

        w_id = self._item["id"]
        if w_id not in map_item:
            map_item[w_id] = {}
        map_item[w_id] = map_item_by_class[self._item["_class"]]
        map_item[w_id]["id"] = w_id
        map_item[w_id]["module"] = self._item["module"]
        map_item[w_id]["abstract"] = self._item["abstract"]
        map_item[w_id]["collection"] = self._item["collection"]
        map_item[w_id]["plural"] = self._item["plural"]
        map_item[w_id]["secureRead"] = self._item["secureRead"]
        map_item[w_id]["secureWrite"] = self._item["secureWrite"]
        map_item[w_id]["_class"] = self._item["_class"]
        map_item[w_id]["_class_obj"] = self._item["_class_obj"]
        map_item[w_id]["father"] = self._item["father"]
        map_item[w_id]["schema"] = self._item["schema"]
        map_item[w_id]["multipart"] = self._item["multipart"]
        map_item[w_id]["isWritable"] = self._item["isWritable"]

        if map_item[w_id]["_class"] not in tree_item.keys():
            tree_item[map_item[w_id]["_class"]] = {}

        tree_item[map_item[w_id]["_class"]]["elem"] = map_item[w_id]

        if "father" in map_item[w_id].keys() and map_item[w_id]["father"] is not None:
            if map_item[w_id]["father"] not in tree_item.keys():
                w_father = tree_item[map_item[w_id]["father"]] = {}
            else:
                w_father = tree_item[map_item[w_id]["father"]]

            if "sons" not in w_father.keys():
                w_father["sons"] = [tree_item[map_item[w_id]["_class"]]]
            else:
                w_father["sons"].append(tree_item[map_item[w_id]["_class"]])
                # create empty
        else:
            tree_item["root"] = tree_item[map_item[w_id]["_class"]]
        _register_class_properties(obj, map_item[w_id])
        return obj


class ItemReference(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, from_name: str, field: str, item: str) -> None:
        self._local_field = field
        self._item_id = item
        self._from_name = from_name

    def __call__(self, obj: type) -> type:
        a_class = _class_name(obj)
        a_item_id = self._item_id
        local_field = self._local_field
        if a_class not in map_item_by_class:
            map_item_by_class[a_class] = {
                "_class": a_class,
                "refs": {},
                "schema": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {},
                },
            }
        w_item = map_item_by_class[a_class]

        if w_item is not None:
            if a_item_id not in w_item["refs"]:
                w_item["refs"][a_item_id] = {
                    "local_field": local_field + ".ref",
                    "foreign_field": "_id",
                    "item_id": a_item_id,
                    "reverse": False,
                }
                w_item["schema"]["properties"][local_field] = {
                    "ref": {
                        "type": "string",
                        "description": "reference to {}".format(a_item_id),
                    }
                }

            # TODO reverse ref
            if a_item_id not in map_item.keys():
                map_item[a_item_id] = {"refs": {}}
            if "refs" not in map_item[a_item_id]:
                map_item[a_item_id]["refs"] = {}
            map_item[a_item_id]["refs"][self._from_name] = {
                "foreign_field": local_field + ".ref",
                "local_field": "_id",
                "item_id": self._from_name,
                "reverse": True,
            }
        return obj


def Empty() -> t.Callable[[t.Callable], t.Callable]:
    """decoration that manage property with another collection"""

    def decorator_property(func: t.Callable) -> t.Callable:
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs) -> t.Any:
            value = func(*args, **kwargs)

            w_item = map_item_by_class[_class_name(type(value))]
            w_item["empty"] = value._mongo_model
            return value

        return wrapper_proprety

    return decorator_property


def Property(
    name: str,
    type: str = "string",
    minLength: int | None = None,
    maxLength: int | None = None,
    minimum: float | None = None,
    exclusiveMinimum: float | None = None,
    maximum: float | None = None,
    exclusiveMaximum: float | None = None,
    private: bool = False,
) -> t.Callable[[t.Callable], t.Callable]:
    """decoration that manage property with another collection"""

    def decorator_property(func: t.Callable) -> t.Callable:
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs) -> t.Any:
            value = func(*args, **kwargs)
            w_name = name

            if "_mongo_model" not in args[0].__dict__:
                args[0]._mongo_model = {}
            if isinstance(args[1], YDict):
                args[0]._mongo_model[w_name] = args[1]._mongo_model
            else:
                args[0]._mongo_model[w_name] = args[1]

            # the type parameter shadows the builtin
            w_class_name = _class_name(args[0].__class__)
            if w_class_name in map_item_by_class:
                _register_property(
                    map_item_by_class[w_class_name],
                    wrapper_proprety._ycappuccino_property,
                )
            return value

        wrapper_proprety._ycappuccino_property = {
            "name": name,
            "private": private,
            "schema": _property_schema(
                name,
                type,
                minLength=minLength,
                maxLength=maxLength,
                minimum=minimum,
                exclusiveMinimum=exclusiveMinimum,
                maximum=maximum,
                exclusiveMaximum=exclusiveMaximum,
            ),
        }
        return wrapper_proprety

    return decorator_property


def Reference(name: str) -> t.Callable[[t.Callable], t.Callable]:
    """decoration that manage reference with another collection"""

    def decorator_reference(func: t.Callable) -> t.Callable:
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs) -> t.Any:
            value = func(*args)
            if args[0] is not None:
                _add_ref(name, args)
            return value

        return wrapper_reference

    return decorator_reference


def _storage_model(a_model: t.Any) -> dict:
    if "_mongo_model" not in a_model.__dict__:
        a_model._mongo_model = {}
    return a_model._mongo_model


def _add_ref(name: str, args: tuple) -> None:
    _storage_model(args[0])[name] = {"ref": args[1]}


def References(name: str) -> t.Callable[[t.Callable], t.Callable]:
    """decoration that manage reference with another collection"""

    def decorator_reference(func: t.Callable) -> t.Callable:
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs) -> t.Any:
            value = func(*args, **kwargs)
            if args[0] is not None:
                w_obj_ref = {"ref": args[1]}
                if len(args) > 2 and isinstance(args[2], dict):
                    # admit dictionnary property of the relation we add it
                    w_obj_ref["properties"] = args[2]
                _storage_model(args[0]).setdefault(name, []).append(w_obj_ref)

                w_item = map_item_by_class.get(_class_name(type(args[0])))
                if w_item is not None:
                    w_item["schema"]["properties"][name] = {
                        "type": "string",
                        "description": "reference to {}".format(name),
                    }
            return value

        return wrapper_reference

    return decorator_reference


def rpc_method(
    method: str = "POST", path: str = "", summary: str = "", secure: bool = True
) -> t.Callable[[t.Callable], t.Callable]:
    """
    marks a method of a component interface as callable from outside the framework (a browser, an HTTP
    client): through __remote_dispatch__ for a framework client, through an HTTP route (method, path)
    otherwise. secure=True: the caller must be authenticated and authorized to "call" it;
    secure=False: the method checks its caller itself. Put it on the interface's abstract method, never
    on an implementation: an implementation cannot widen the public surface. The method is returned
    unchanged, only annotated.
    """

    def decorator(func: t.Callable) -> t.Callable:
        try:
            hints = t.get_type_hints(func)
        except Exception:
            hints = dict(getattr(func, "__annotations__", {}))
        parameters = [name for name in inspect.signature(func).parameters if name != "self"]
        func._ycappuccino_rpc_method = {
            "method": method,
            "path": path,
            "summary": summary,
            "secure": secure,
            "params": {name: hints[name] for name in parameters if name in hints},
            "return_type": hints.get("return"),
        }
        return func

    return decorator


def get_rpc_methods(klass: type) -> dict:
    """method name -> @rpc_method metadata, for klass and every class it inherits from"""
    methods = {}
    for base in reversed(klass.__mro__):
        for name, attribute in vars(base).items():
            metadata = getattr(attribute, "_ycappuccino_rpc_method", None)
            if metadata is not None:
                methods[name] = metadata
    return methods


primitive = (
    int,
    str,
    bool,
    float,
)

# identified item by id
map_item: dict[str, dict] = {}
# manage tree of item to have dependencies
tree_item: dict[str, t.Any] = {}
# identified item by qualified class name (module.QualName)
map_item_by_class: dict[str, dict] = {}


def get_item_by_class(a_class: type) -> dict:
    return map_item_by_class[_class_name(a_class)]


def get_item(a_id: str) -> dict:
    return map_item[a_id]


def get_tree_item() -> dict:
    return tree_item


def get_bundle_model_ordered() -> list:
    w_root = tree_item["root"]
    w_ordered_list = []
    w_ordered_list.append("ycappuccino.api.decorators")
    w_ordered_list.append("ycappuccino.api.models")
    w_ordered_list.append("ycappuccino.core.decorator_app")
    for w_item in get_bundle_model(w_root):
        w_ordered_list.append(w_item)

    return w_ordered_list


def get_bundle_model(a_tree_item: dict) -> list:
    w_ordered_list = []
    w_ordered_list.append(a_tree_item["elem"]["_class_obj"].__module__)
    if "sons" in a_tree_item.keys():
        for w_item in a_tree_item["sons"]:
            for w_son_module in get_bundle_model(w_item):
                w_ordered_list.append(w_son_module)

    return w_ordered_list


def get_map_items() -> list:
    w_items = []
    for w_key in map_item:
        w_items.append(map_item[w_key])
    return w_items


def get_map_items_emdpoint() -> list:
    w_items = []
    for w_key in map_item:
        w_dict = map_item[w_key].copy()
        del w_dict["_class"]
        w_dict["python_module"] = w_dict["_class_obj"].__module__
        del w_dict["_class_obj"]

        w_items.append(w_dict)
    return w_items


def has_father_item(a_item_id: str) -> bool:
    return map_item[a_item_id].get("father") is not None


def get_sons_item(a_item_id: str) -> list:
    w_father_class = map_item[a_item_id]["_class"]
    return [
        w_item for w_item in map_item.values() if w_item.get("father") == w_father_class
    ]


def get_sons_item_id(a_item_id: str) -> list:
    w_list_son = [a_item_id]
    w_item_father = map_item[a_item_id]
    for w_item in map_item.values():
        if (
            "father" in w_item.keys()
            and w_item["father"] is not None
            and w_item["father"] == w_item_father["_class"]
        ):
            w_list_son.append(w_item["id"])
    return w_list_son


if __name__ == "__main__":

    @Item(collection="col", name="name", plural="names")
    class Test(object):

        def __init__(self) -> None:
            self._toto = "toto"
            self._name = None

        @Property(name="foo")
        def name(self, a_value: t.Any) -> None:
            self._name = a_value

    test = Test()
    test.name("test")
    print(test.__dict__)

    test2 = Test()
    test2.name(test)
    print(test2.__dict__)

"""

list of decorator for declaring models in application in a ORM Ycappuccino mechanism
"""

import typing as t

# decorators to describe item and element to store in mongo if it's mongo element
import functools


class YDict(object):

    def __init__(self, *a_tuple):
        for t in a_tuple:
            if isinstance(t, dict):
                for k, v in t.items():
                    setattr(self, k, v)


class Item(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(
        self,
        collection,
        name,
        plural,
        abstract=False,
        module="system",
        app="ycappuccino_core",
        secure_read=False,
        secure_write=False,
        is_writable=True,
        multipart=None,
    ):
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

    def __call__(self, obj):
        self._super_class = (
            obj.__bases__[0].__name__
            if len(obj.__bases__) > 0 and obj.__bases__[0].__name__ != "YDict"
            else None
        )
        self._class = obj.__name__
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
        return obj


class ItemReference(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, from_name, field, item):
        self._local_field = field
        self._item_id = item
        self._from_name = from_name

    def __call__(self, obj):
        a_class = obj.__name__
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


def Empty():
    """decoration that manage property with another collection"""

    def decorator_property(func):
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs):
            value = func(*args, **kwargs)

            w_item = map_item_by_class[value.__class__.__name__]
            w_item["empty"] = value._mongo_model
            return value

        return wrapper_proprety

    return decorator_property


def Property(
    name,
    type="string",
    minLength=None,
    maxLength=None,
    minimum=None,
    exclusiveMinimum=None,
    maximum=None,
    exclusiveMaximum=None,
    private=False,
):
    """decoration that manage property with another collection"""

    def decorator_property(func):
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs):
            value = func(*args, **kwargs)
            w_name = name

            if "_mongo_model" not in args[0].__dict__:
                args[0]._mongo_model = {}
            if isinstance(args[1], YDict):
                args[0]._mongo_model[w_name] = args[1]._mongo_model
            else:
                args[0]._mongo_model[w_name] = args[1]

            if args[0].__class__.__name__ in map_item_by_class:
                w_item = map_item_by_class[args[0].__class__.__name__]
                w_item["schema"]["properties"][w_name] = {
                    "type": type,
                    "description": "{}".format(w_name),
                }

                if minLength:
                    w_item["schema"]["properties"][w_name]["minLength"] = minLength

                if maxLength:
                    w_item["schema"]["properties"][w_name]["maxLength"] = maxLength

                if minimum:
                    w_item["schema"]["properties"][w_name]["minimum"] = minimum

                if exclusiveMinimum:
                    w_item["schema"]["properties"][w_name][
                        "exclusiveMinimum"
                    ] = exclusiveMinimum

                if maximum:
                    w_item["schema"]["properties"][w_name]["maximum"] = maximum

                if exclusiveMaximum:
                    w_item["schema"]["properties"][w_name][
                        "exclusiveMaximum"
                    ] = exclusiveMaximum

                if "private_property" not in w_item:
                    w_item["private_property"] = []
                if private and name not in w_item["private_property"]:
                    w_item["private_property"].append(w_name)
            return value

        return wrapper_proprety

    return decorator_property


def Reference(name):
    """decoration that manage reference with another collection"""

    def decorator_reference(func):
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs):
            value = func(*args)
            if args[0] is not None:
                _add_ref(name, args)
            return value

        return wrapper_reference

    return decorator_reference


def _add_ref(name, args):
    w_model = args[0]
    w_ref_val = args[1]
    if isinstance(w_model, YDict):
        if "_mongo_model" not in w_model.__dict__:
            w_model["_mongo_model"] = {}
        w_model.__dict__["_mongo_model"][name] = {"ref": w_ref_val}
    else:
        w_model[name]["ref"] = w_ref_val
    # TODO property


def References(name):
    """decoration that manage reference with another collection"""

    def decorator_reference(func):
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs):
            value = func(*args)
            if args[0] is not None:
                if "_mongo_model" not in args[0].__dict__:
                    args[0]._mongo_model = {}

                if name not in args[0]._mongo_model:
                    args[0]._mongo_model[name] = []

                w_obj_ref = _add_ref(args)

                args[0]._mongo_model[name].append(w_obj_ref)

                if len(args) > 2 and isinstance(args[2], dict):
                    # admit dictionnary property of the relation we add it
                    w_obj_ref["properties"] = args[2]

                w_item = map_item_by_class[args[0].__name__]
                w_item["schema"]["properties"][name] = {
                    "type": "string",
                    "description": "reference to {}".format(name),
                }
            return value

        return wrapper_reference

    return decorator_reference


primitive = (
    int,
    str,
    bool,
    float,
)

# identified item by id
map_item: dict[str, Item] = {}
# manage tree of item to have dependencies
tree_item: dict[str, t.Any] = {}
# identified item by class name
map_item_by_class: dict[str, Item] = {}


def get_item_by_class(a_class):
    return map_item_by_class[a_class.__name__]


def get_item(a_id):
    return map_item[a_id]


def get_tree_item():
    return tree_item


def get_bundle_model_ordered():
    w_root = tree_item["root"]
    w_ordered_list = []
    w_ordered_list.append("ycappuccino_storage.ycappuccino_core.models.decorators")
    w_ordered_list.append("ycappuccino_storage.ycappuccino_core.models.utils")
    w_ordered_list.append("ycappuccino_storage.ycappuccino_core.decorator_app")
    for w_item in get_bundle_model(w_root):
        w_ordered_list.append(w_item)

    return w_ordered_list


def get_bundle_model(a_tree_item):
    w_ordered_list = []
    w_ordered_list.append(a_tree_item["elem"]["_class_obj"].__module__)
    if "sons" in a_tree_item.keys():
        for w_item in a_tree_item["sons"]:
            for w_son_module in get_bundle_model(w_item):
                w_ordered_list.append(w_son_module)

    return w_ordered_list


def get_map_items():
    w_items = []
    for w_key in map_item:
        w_items.append(map_item[w_key])
    return w_items


def get_map_items_emdpoint():
    w_items = []
    for w_key in map_item:
        w_dict = map_item[w_key].copy()
        del w_dict["_class"]
        w_dict["python_module"] = w_dict["_class_obj"].__module__
        del w_dict["_class_obj"]

        w_items.append(w_dict)
    return w_items


def has_father_item(a_item_id):
    return map_item[a_item_id].father is not None


def get_sons_item(a_item_id):
    w_list_son = []
    for w_item in map_item.values():
        if w_item.father == a_item_id:
            w_list_son.append(w_item)
    return w_list_son


def get_sons_item_id(a_item_id):
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

        def __init__(self):
            self._toto = "toto"
            self._name = None

        @Property(name="foo")
        def name(self, a_value):
            self._name = a_value

    test = Test()
    test.name("test")
    print(test.__dict__)

    test2 = Test()
    test2.name(test)
    print(test2.__dict__)

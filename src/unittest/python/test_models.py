import unittest

from ycappuccino.api.decorators import (
    Empty,
    Item,
    Property,
    Reference,
    References,
    YDict,
    get_bundle_model_ordered,
    get_item,
    get_item_by_class,
    get_sons_item,
    get_sons_item_id,
    has_father_item,
)
from ycappuccino.api.models import Model


@Item(collection="books", name="book", plural="books")
class Book(Model):

    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._title = None
        self._pages = None
        self._author = None

    @Property(name="title", minLength=0, maxLength=120)
    def title(self, a_value):
        self._title = a_value

    @Property(name="pages", type="integer", minimum=0, maximum=5000)
    def pages(self, a_value):
        self._pages = a_value

    @Reference(name="author")
    def author(self, a_value):
        self._author = a_value

    @References(name="tags")
    def tags(self, a_value, a_properties=None):
        pass


@Item(collection="books", name="novel", plural="novels")
class Novel(Book):
    pass


class Plain(YDict):

    @Reference(name="owner")
    def owner(self, a_value):
        pass


@Item(collection="eager_accounts", name="eager_account", plural="eager_accounts")
class EagerAccount(Model):

    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._login = None
        self._password = None

    @Property(name="login", minLength=3)
    def login(self, a_value):
        self._login = a_value

    @Property(name="password", private=True)
    def password(self, a_value):
        self._password = a_value


@Empty()
def empty_book():
    book = Book()
    book.id("empty")
    return book


class TestModelProperties(unittest.TestCase):

    def test_property_is_stored_in_storage_model(self):
        book = Book()
        book.title("Dune")

        self.assertEqual(book.get_storage_model(), {"title": "Dune"})

    def test_schema_keeps_zero_constraints(self):
        Book().pages(10)

        schema = get_item("book")["schema"]["properties"]
        self.assertEqual(schema["pages"]["minimum"], 0)
        self.assertEqual(schema["pages"]["maximum"], 5000)
        self.assertEqual(schema["title"]["minLength"], 0)

    def test_reference_is_stored_as_ref(self):
        book = Book()
        book.author("herbert")

        self.assertEqual(book.get_storage_model()["author"], {"ref": "herbert"})

    def test_reference_on_ydict_without_storage_model(self):
        plain = Plain()
        plain.owner("alice")

        self.assertEqual(plain._mongo_model, {"owner": {"ref": "alice"}})

    def test_references_accumulate_with_optional_properties(self):
        book = Book()
        book.tags("sf")
        book.tags("classic", {"weight": 2})

        self.assertEqual(
            book.get_storage_model()["tags"],
            [{"ref": "sf"}, {"ref": "classic", "properties": {"weight": 2}}],
        )

    def test_empty_model_is_registered(self):
        empty_book()

        self.assertEqual(get_item("book")["empty"], {"_id": "empty"})


class TestItemRegistry(unittest.TestCase):

    def test_item_is_registered_by_id_and_class(self):
        self.assertEqual(get_item("book")["collection"], "books")
        self.assertIs(get_item_by_class(Book), get_item("book"))

    def test_has_father_item(self):
        self.assertTrue(has_father_item("novel"))
        self.assertFalse(has_father_item("models"))

    def test_get_sons_item(self):
        self.assertEqual([item["id"] for item in get_sons_item("book")], ["novel"])

    def test_get_sons_item_id(self):
        self.assertEqual(get_sons_item_id("book"), ["book", "novel"])

    def test_bundle_model_ordered_starts_with_framework_modules(self):
        ordered = get_bundle_model_ordered()

        self.assertEqual(
            ordered[:3],
            [
                "ycappuccino.api.decorators",
                "ycappuccino.api.models",
                "ycappuccino.core.decorator_app",
            ],
        )
        self.assertIn(__name__, ordered)


class TestSchemaDeclaration(unittest.TestCase):

    def test_schema_is_known_before_any_instance(self):
        properties = get_item("eager_account")["schema"]["properties"]

        self.assertEqual(properties["login"], {"type": "string", "description": "login", "minLength": 3})
        self.assertIn("_id", properties)

    def test_private_properties_are_known_before_any_instance(self):
        self.assertEqual(get_item("eager_account")["private_property"], ["password"])


if __name__ == "__main__":
    unittest.main()

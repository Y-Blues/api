import unittest

import collision_models
import test_models

from ycappuccino.api.decorators import get_item, get_item_by_class, get_sons_item_id


class TestRegistryWithHomonymClasses(unittest.TestCase):

    def test_items_of_homonym_classes_stay_distinct(self):
        self.assertEqual(get_item("book")["collection"], "books")
        self.assertEqual(get_item("collision_book")["collection"], "collision_books")

    def test_item_by_class_uses_the_module_of_the_class(self):
        self.assertIs(get_item_by_class(test_models.Book), get_item("book"))
        self.assertIs(get_item_by_class(collision_models.Book), get_item("collision_book"))

    def test_sons_are_the_subclasses_of_the_item_class(self):
        self.assertEqual(get_sons_item_id("book"), ["book", "novel"])
        self.assertEqual(get_sons_item_id("collision_book"), ["collision_book", "collision_novel"])

    def test_schemas_of_homonym_classes_stay_distinct(self):
        self.assertNotIn("label", get_item("book")["schema"]["properties"])
        self.assertIn("label", get_item("collision_book")["schema"]["properties"])


if __name__ == "__main__":
    unittest.main()

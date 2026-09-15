"""
Models whose classes are named like the models of test_models, declared in another module.
"""

from ycappuccino.api.decorators import Item, Property
from ycappuccino.api.models import Model


@Item(collection="collision_books", name="collision_book", plural="collision_books")
class Book(Model):

    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._label = None

    @Property(name="label", private=True)
    def label(self, a_value):
        self._label = a_value


@Item(collection="collision_books", name="collision_novel", plural="collision_novels")
class Novel(Book):
    pass

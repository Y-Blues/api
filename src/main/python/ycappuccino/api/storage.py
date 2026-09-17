# app="all"
"""
storage api: persistence of the models declared with @Item

A subject is the dict decoded from the JWT: {"sub": <account id>, "tid": <tenant id>}.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ycappuccino.api.core_base import YCappuccinoComponent
from ycappuccino.api.models import Model


class IStorage(YCappuccinoComponent, ABC):
    """persistence backend working on collections of documents"""

    @abstractmethod
    async def get_one(self, collection: str, query: dict) -> Optional[dict]:
        """first document matching the query, or None"""

    @abstractmethod
    async def get_many(
        self,
        collection: str,
        query: dict,
        offset: int = 0,
        limit: Optional[int] = 50,
        sort: Optional[dict] = None,
    ) -> list:
        """documents matching the query; limit None means no limit; sort maps a field to 1 or -1"""

    @abstractmethod
    async def up_sert(
        self, collection: str, id: str, document: dict, on_insert: Optional[dict] = None
    ) -> dict:
        """set the fields of document on the document id, created with on_insert fields when missing; return the stored document"""

    @abstractmethod
    async def delete(self, collection: str, query: dict) -> int:
        """delete the documents matching the query and return their number"""

    @abstractmethod
    async def count(self, collection: str, query: dict) -> int:
        """number of documents matching the query"""


class IItemManager(YCappuccinoComponent, ABC):
    """metadata of the items declared with @Item"""

    @abstractmethod
    def get_items(self) -> list:
        """non abstract items"""

    @abstractmethod
    def get_item(self, item_id: str) -> dict:
        """item metadata; KeyError when unknown"""

    @abstractmethod
    def get_item_by_plural(self, plural: str) -> dict:
        """item metadata by plural name; KeyError when unknown"""

    @abstractmethod
    def get_sons_item_ids(self, item_id: str) -> list:
        """the item id followed by the ids of all its descendants"""

    @abstractmethod
    def get_schema(self, item_id: str) -> dict:
        """json schema of the item"""

    @abstractmethod
    def get_empty(self, item_id: str) -> Optional[dict]:
        """storage model of the empty instance of the item, or None"""


class IManager(YCappuccinoComponent, ABC):
    """generic manager of the items: the item id is given to every operation"""

    @abstractmethod
    async def get_one(
        self, item_id: str, id: str, params: Optional[dict] = None, subject: Optional[dict] = None
    ) -> Optional[Model]:
        """model of the item with this id, or None"""

    @abstractmethod
    async def get_many(
        self, item_id: str, params: Optional[dict] = None, subject: Optional[dict] = None
    ) -> list:
        """models matching params (filter, sort, limit, offset, expand, content)"""

    @abstractmethod
    async def up_sert(
        self, item_id: str, id: str, fields: dict, subject: Optional[dict] = None
    ) -> Model:
        """create or update the item id from fields and return the stored model"""

    @abstractmethod
    async def up_sert_model(self, model: Model, subject: Optional[dict] = None) -> Model:
        """create or update a model (its _id is required) and return the stored model"""

    @abstractmethod
    async def delete(self, item_id: str, id: str, subject: Optional[dict] = None) -> None:
        """delete the item id if it exists"""

    @abstractmethod
    async def delete_many(
        self, item_id: str, query: dict, subject: Optional[dict] = None
    ) -> int:
        """delete the items matching the query and return their number"""

    @abstractmethod
    async def count(self, item_id: str, params: Optional[dict] = None, subject: Optional[dict] = None) -> int:
        """number of models get_many would return without offset and limit"""


class ITrigger(YCappuccinoComponent, ABC):
    """called around the operations on one item"""

    # item watched (exact item id, sons are not included)
    item_id: str = ""
    # operations watched among "read", "upsert", "delete"
    actions: tuple = ()
    # True: called after the operation, False: called before and can abort it
    post: bool = True

    @abstractmethod
    async def execute(self, action: str, item_id: str, model: Model) -> None:
        """react to the operation on the model"""


class IFilter(YCappuccinoComponent, ABC):
    """adds conditions to the queries of a subject (e.g. multi tenancy)"""

    @abstractmethod
    async def get_filter(self, item_id: str, subject: dict) -> Optional[dict]:
        """condition added to the queries on the item for the subject, or None"""


class IFileStore(YCappuccinoComponent, ABC):
    """storage of the uploaded contents"""

    @abstractmethod
    async def put(self, key: str, content: bytes) -> None:
        """store the content under the key"""

    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        """content stored under the key, or None"""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """delete the content stored under the key if it exists"""

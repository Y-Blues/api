"""
endpoints_storage api: use cases on the models declared with @Item, independent of any transport.

A subject is the dict decoded from the JWT: {"sub": <account id>, "tid": <tenant id>}, or None when anonymous.
Results are serializable dicts; failures are CrudError subclasses that the adapters translate.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ycappuccino.api.core_base import YCappuccinoComponent

# actions checked by IAuthorization
READ = "read"
WRITE = "write"
DELETE = "delete"
PRIVATE = "private"


class CrudError(Exception):
    """failure of a use case, translated by the adapters"""


class NotAuthenticated(CrudError):
    """secured action without subject (HTTP 401)"""


class Forbidden(CrudError):
    """read-only item, or subject not authorized (HTTP 403)"""


class NotFound(CrudError):
    """unknown or abstract item, missing document or draft (HTTP 404)"""


class InvalidRequest(CrudError):
    """invalid parameters, id or fields (HTTP 400)"""


class ICrud(YCappuccinoComponent, ABC):
    """reads and writes of the documents of an item; drafts are excluded"""

    @abstractmethod
    async def get_one(
        self, item_id: str, id: str, params: Optional[dict] = None, subject: Optional[dict] = None
    ) -> dict:
        """document id; NotFound when missing"""

    @abstractmethod
    async def get_many(self, item_id: str, params: Optional[dict] = None, subject: Optional[dict] = None) -> dict:
        """{"items": documents matching params, "total": number of matching documents}"""

    @abstractmethod
    async def create(self, item_id: str, fields: dict, subject: Optional[dict] = None) -> dict:
        """upsert the document fields["_id"], or a new uuid, and return it"""

    @abstractmethod
    async def update(self, item_id: str, id: str, fields: dict, subject: Optional[dict] = None) -> dict:
        """upsert the fields of the document id and return it"""

    @abstractmethod
    async def delete(self, item_id: str, id: str, subject: Optional[dict] = None) -> None:
        """delete the document id and its drafts; NotFound when missing"""

    @abstractmethod
    async def delete_many(self, item_id: str, filter: dict, subject: Optional[dict] = None) -> int:
        """delete the documents matching the non empty filter, and their drafts; return their number"""


class IDrafts(YCappuccinoComponent, ABC):
    """named drafts of the documents of an item"""

    @abstractmethod
    async def get_one(
        self, item_id: str, id: str, draft: str, params: Optional[dict] = None, subject: Optional[dict] = None
    ) -> dict:
        """draft version of the document id, else the document; NotFound when both are missing"""

    @abstractmethod
    async def get_many(
        self, item_id: str, draft: str, params: Optional[dict] = None, subject: Optional[dict] = None
    ) -> dict:
        """{"items", "total"} where the documents having the draft are replaced by their draft version"""

    @abstractmethod
    async def save(self, item_id: str, id: str, draft: str, fields: dict, subject: Optional[dict] = None) -> dict:
        """upsert the draft of the document id and return its draft version"""

    @abstractmethod
    async def publish(self, item_id: str, id: str, draft: str, subject: Optional[dict] = None) -> dict:
        """write the draft on the document id, delete the draft and return the document"""

    @abstractmethod
    async def discard(self, item_id: str, id: str, draft: str, subject: Optional[dict] = None) -> None:
        """delete the draft of the document id; NotFound when missing"""


class IItemCatalog(YCappuccinoComponent, ABC):
    """metadata of the items readable by a subject"""

    @abstractmethod
    async def get_items(self, subject: Optional[dict] = None) -> list:
        """public metadata of the non abstract items readable by the subject"""

    @abstractmethod
    async def get_item(self, item_id: str, subject: Optional[dict] = None) -> dict:
        """public metadata of the item"""

    @abstractmethod
    async def get_item_by_plural(self, plural: str, subject: Optional[dict] = None) -> dict:
        """public metadata of the item with this plural name"""

    @abstractmethod
    async def get_schema(self, item_id: str, subject: Optional[dict] = None) -> dict:
        """json schema of the item"""

    @abstractmethod
    async def get_empty(self, item_id: str, subject: Optional[dict] = None) -> Optional[dict]:
        """storage model of the empty instance of the item, or None"""


class IAuthorization(YCappuccinoComponent, ABC):
    """decides whether a subject may perform an action on an item"""

    @abstractmethod
    async def is_authorized(self, subject: dict, action: str, item_id: str) -> bool:
        """action among READ, WRITE, DELETE and PRIVATE"""

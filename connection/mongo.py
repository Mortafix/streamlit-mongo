from typing import Dict, List, Union

from pymongo import MongoClient
from streamlit.connections import BaseConnection
from streamlit.runtime.caching import cache_data


class MongoDBConnection(BaseConnection[MongoClient]):
    def _connect(self, **kwargs) -> MongoClient:
        db = kwargs.pop("database", None) or self._secrets.get("database")
        coll = kwargs.pop("collection", None) or self._secrets.get("collection")
        parameters = {**self._secrets.get("kwargs", {}), **kwargs}
        client = MongoClient(self._secrets.get("url"), **parameters)
        return client[db][coll]

    # find

    def find(
        self,
        filters: dict = None,
        one: bool = False,
        mongo_id: bool = False,
        ttl: int = 3600,
        **kwargs
    ) -> Union[List, Dict]:
        """Find documents in the MongoDB collection that match the provided filters.
        If 'one' is True, only the first match will be returned.
        If 'mongo_id' is False, the Mongo ID will be excluded from the results."""

        @cache_data(ttl=ttl)
        def _find(filters: dict, **kwargs):
            mongo_id_proj = {"_id": 0} if not mongo_id else {}
            kwargs["projection"] = kwargs.get("projection", {}) | mongo_id_proj
            if one:
                return self._instance.find_one(filters or {}, **kwargs)
            return list(self._instance.find(filters or {}, **kwargs))

        return _find(filters, **kwargs)

    def find_one(
        self, filters: dict = None, mongo_id: bool = False, ttl: int = 3600, **kwargs
    ) -> Dict:
        """Find a single document in the MongoDB collection that matches the provided
        filters. If 'mongo_id' is False, the Mongo ID will be excluded from
        the results."""
        return self.find(filters, one=True, mongo_id=mongo_id, ttl=ttl, **kwargs)

    # insert

    def insert(self, data: Union[List, Dict], ttl: int = 0, **kwargs) -> Dict:
        """Insert the provided data into the MongoDB collection.
        The data can be a single document (Dict) or multiple documents (List)."""

        @cache_data(ttl=ttl)
        def _insert_many(data: List, **kwargs):
            response = self._instance.insert_many(data, **kwargs)
            return {"inserted_ids": response.inserted_ids}

        @cache_data(ttl=ttl)
        def _insert_one(data: Dict, **kwargs):
            response = self._instance.insert_one(data, **kwargs)
            return {"inserted_id": response.inserted_id}

        if isinstance(data, Dict):
            return _insert_one(data, **kwargs)
        return _insert_many(data, **kwargs)

    # update

    def update(
        self, filters: Dict, data: Dict, one: bool = False, ttl: int = 0, **kwargs
    ) -> Dict:
        """Update the documents in the MongoDB collection that match the provided
        filters with the provided data. If 'one' is True, only the first matching
        document will be updated."""

        @cache_data(ttl=ttl)
        def _update(filters: Dict, data: Dict, **kwargs):
            response = (
                self._instance.update_one(filters, data, **kwargs)
                if one
                else self._instance.update_many(filters, data, **kwargs)
            )
            return {
                "matched_count": response.matched_count,
                "modified_count": response.modified_count,
                "upserted_id": response.upserted_id,
            }

        return _update(filters, data, **kwargs)

    def update_one(self, filters: Dict, data: Dict, ttl: int = 0, **kwargs) -> Dict:
        """Update a single document in the MongoDB collection that matches the provided
        filters with the provided data."""
        return self.update(filters, data, one=True, ttl=ttl, **kwargs)

    # delete

    def delete(self, filters: Dict, one: bool = False, ttl: int = 0, **kwargs) -> Dict:
        """Delete documents in the MongoDB collection that match the provided filters.
        If 'one' is True, only the first matching document will be deleted."""

        @cache_data(ttl=ttl)
        def _delete(filters: Dict, **kwargs):
            response = (
                self._instance.delete_one(filters, **kwargs)
                if one
                else self._instance.delete_many(filters, **kwargs)
            )
            return {"deleted_count": response.deleted_count}

        return _delete(filters, **kwargs)

    def delete_one(self, filters: Dict, ttl: int = 0, **kwargs) -> Dict:
        """Delete a single document in the MongoDB collection that matches the
        provided filters."""
        return self.delete(filters, one=True, ttl=ttl, **kwargs)

    # extra

    def replace(
        self, filters: Dict = None, replacement: Dict = None, ttl: int = 0, **kwargs
    ) -> Dict:
        """Replace a single document in the MongoDB collection that matches the
        provided filters with the provided replacement."""

        @cache_data(ttl=ttl)
        def _replace(filters: Dict, replacement: Dict, **kwargs):
            response = self._instance.replace_one(filters or {}, replacement, **kwargs)
            return {
                "matched_count": response.matched_count,
                "modified_count": response.modified_count,
                "upserted_id": response.upserted_id,
            }

        return _replace(filters, replacement, **kwargs)

    def aggregate(self, pipeline: Dict, ttl: int = 3600, **kwargs) -> List:
        """Aggregate the data in the MongoDB collection using the provided
        aggregation pipeline."""

        @cache_data(ttl=ttl)
        def _aggregate(pipeline: Dict, **kwargs):
            return list(self._instance.aggregate(pipeline or {}, **kwargs))

        return _aggregate(pipeline, **kwargs)

    def count(self, filters: Dict = None, ttl: int = 3600, **kwargs) -> int:
        """Count the number of documents in the MongoDB collection that match the
        provided filters."""

        @cache_data(ttl=ttl)
        def _count(filters: Dict, **kwargs):
            return self._instance.count_documents(filters or {}, **kwargs)

        return _count(filters, **kwargs)

    def distinct(
        self, field: str, filters: Dict = None, ttl: int = 3600, **kwargs
    ) -> List:
        """Find the distinct values for a specified field across a single collection
        and returns the results in an array."""

        @cache_data(ttl=ttl)
        def _distinct(filters: Dict, **kwargs):
            return self._instance.distinct(field, filters or {}, **kwargs)

        return _distinct(filters, **kwargs)

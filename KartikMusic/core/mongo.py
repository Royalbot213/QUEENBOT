from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
# MONGO_DB_NAME is optional in config; load if present
try:
    from config import MONGO_DB_NAME
except Exception:
    MONGO_DB_NAME = None

# Try to import project LOGGER factory, but fall back to stdlib logging if unavailable
try:
    from ..logging import LOGGER
except Exception:
    from logging import getLogger
    LOGGER = lambda name: getLogger(name)

logger = LOGGER(__name__)

class MongoDB:
    """Simple wrapper around AsyncIOMotorClient + Database.

    Usage:
      - Import the class: from KartikMusic.core.mongo import MongoDB
      - Use the module-level `mongodb` Database-like object for backwards compatibility.
    """
    def __init__(self, uri: str = None, db_name: str = None):
        self._uri = uri or MONGO_DB_URI
        self._db_name = db_name or MONGO_DB_NAME
        self.client = None
        self.db = None

    def connect(self):
        """Create AsyncIOMotorClient and set the `db` attribute to a Database object.
        This is synchronous and safe to call at import time (the client does not block).
        """
        if self.client is None:
            if not self._uri:
                raise RuntimeError("MONGO_DB_URI is not set in config")
            self.client = AsyncIOMotorClient(self._uri)
            # Prefer DB from URI if present
            self.db = self.client.get_default_database()
            if self.db is None:
                if self._db_name:
                    self.db = self.client[self._db_name]
                else:
                    logger.warning(
                        "No default DB found in MONGO_DB_URI and MONGO_DB_NAME not set in config; using 'Anon'."
                    )
                    self.db = self.client["Anon"]
            logger.info("Connected to Mongo Database: %s", self.db.name)

    def get_db(self):
        if self.db is None:
            self.connect()
        return self.db


# Module-level instance for backward compatibility with code that imports `mongodb`.
try:
    _default_client = AsyncIOMotorClient(MONGO_DB_URI)
    _default_db = _default_client.get_default_database()
    if _default_db is None:
        if MONGO_DB_NAME:
            _default_db = _default_client[MONGO_DB_NAME]
        else:
            logger.warning(
                "No default DB found in MONGO_DB_URI and MONGO_DB_NAME not set in config; using 'Anon'."
            )
            _default_db = _default_client["Anon"]
    mongodb = _default_db
except Exception as exc:
    # If the import-time setup fails (e.g., missing config), create a lazy wrapper
    logger.exception("Mongo setup at import failed: %s", exc)
    # Provide a MongoDB instance that will raise useful errors when used
    mongodb = MongoDB()

# Also export the MongoDB class
__all__ = ["MongoDB", "mongodb"]

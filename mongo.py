from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
# MONGO_DB_NAME is optional in config; load if present
try:
    from config import MONGO_DB_NAME
except Exception:
    MONGO_DB_NAME = None

# If your project provides a LOGGER factory like before, keep the relative import.
# If that import fails in your package layout, replace with Python's logging (example below).
from ..logging import LOGGER

logger = LOGGER(__name__)

logger.info("Connecting to your Mongo Database...")
try:
    _mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
    # Try to get the database from the URI first (if URI contains /dbname)
    mongodb = _mongo_client.get_default_database()

    # If no DB in URI, use MONGO_DB_NAME from config if provided
    if mongodb is None:
        if MONGO_DB_NAME:
            mongodb = _mongo_client[MONGO_DB_NAME]
        else:
            logger.warning(
                "No default DB found in MONGO_DB_URI and MONGO_DB_NAME not set in config; using 'Anon'."
            )
            mongodb = _mongo_client["Anon"]

    logger.info("Connected to your Mongo Database: %s", mongodb.name)
except Exception as exc:
    # Log full traceback and re-raise so the app can handle it (avoid silent exit())
    logger.exception("Failed to connect to your Mongo Database: %s", exc)
    raise

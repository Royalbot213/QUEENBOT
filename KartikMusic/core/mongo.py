from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
try:
    from config import MONGO_DB_NAME
except Exception:
    MONGO_DB_NAME = None

from ..logging import LOGGER
logger = LOGGER(__name__)

logger.info("Connecting to your Mongo Database...")
try:
    _mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_client.get_default_database()

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
    logger.exception("Failed to connect to your Mongo Database: %s", exc)
    raise

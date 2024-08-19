from api.utils.logger import ilogger
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from api.config import settings


async def init_db():
    # Async MongoDB Client
    client = AsyncIOMotorClient(settings.DATABASE_URI)

    # Documents
    from api.user.user_model import User

    # Init Beanie ODM
    ilogger.info("Waiting for database startup.")
    await init_beanie(
        database=client.get_database(settings.DATABASE_NAME), document_models=[User]
    )
    ilogger.info("Database startup complete.")

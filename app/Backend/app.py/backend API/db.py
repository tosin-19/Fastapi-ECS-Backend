from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

settings = get_settings()
client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB]

# Collections
users_coll = db["users"]
posts_coll = db["posts"]
files_coll = db["files"]

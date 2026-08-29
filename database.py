from pymongo import AsyncMongoClient
from config import MONGO_URI, MONGO_DB_NAME

_client = AsyncMongoClient(MONGO_URI)
db = _client[MONGO_DB_NAME]

async def init():
    await db.authorized_users.create_index("user_id", unique=True)
    await db.telegram_sessions.create_index("user_id", unique=True)
    await db.active_tasks.create_index("user_id", unique=True)
    await db.worker_state.create_index("user_id", unique=True)

def col(name):
    return db[name]

async def authorize(user_id):
    await col("authorized_users").update_one({"user_id": user_id}, {"$set": {"enabled": True}}, upsert=True)

async def deauthorize(user_id):
    await col("authorized_users").update_one({"user_id": user_id}, {"$set": {"enabled": False}})

async def is_authorized(user_id):
    doc = await col("authorized_users").find_one({"user_id": user_id, "enabled": True})
    return bool(doc)

async def list_authorized():
    return [x["user_id"] async for x in col("authorized_users").find({"enabled": True}, {"user_id": 1})]

async def get_session(user_id):
    doc = await col("telegram_sessions").find_one({"user_id": user_id}, {"session": 1})
    return doc.get("session") if doc else None

async def set_session(user_id, session):
    await col("telegram_sessions").update_one({"user_id": user_id}, {"$set": {"session": session}}, upsert=True)

async def clear_task(user_id):
    await col("active_tasks").delete_one({"user_id": user_id})

async def stats(user_id):
    user = await col("stats").find_one({"_id": user_id}) or {}
    global_ = await col("stats").find_one({"_id": "global"}) or {}
    return user, global_

async def bump(user_id, field):
    await col("stats").update_one({"_id": user_id}, {"$inc": {field: 1}}, upsert=True)
    await col("stats").update_one({"_id": "global"}, {"$inc": {field: 1}}, upsert=True)

async def get_global_enabled():
    doc = await col("worker_state").find_one({"_id": "global"})
    return doc.get("enabled", True) if doc else True

async def set_global_enabled(value):
    await col("worker_state").update_one({"_id": "global"}, {"$set": {"enabled": value}}, upsert=True)

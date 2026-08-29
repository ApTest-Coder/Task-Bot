import asyncio
from pyrogram import Client, filters
from pyrogram.errors import RPCError

import database
from config import API_ID, API_HASH, BOT_TOKEN, DEVELOPER_USERNAME, LOG_CHANNEL_ID, OWNER_ID, OWNER_SESSION

clients = {}
worker_tasks = {}
global_tasks = True
started_at = asyncio.get_event_loop().time()

bot = Client("taskbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def owner(message):
    return message.from_user and message.from_user.id == OWNER_ID

async def send_log(text):
    if LOG_CHANNEL_ID:
        await bot.send_message(LOG_CHANNEL_ID, text)

async def start_user(user_id, session):
    if user_id in clients:
        return clients[user_id]
    client = Client(f"user_{user_id}", api_id=API_ID, api_hash=API_HASH, session_string=session)
    await client.start()
    clients[user_id] = client
    return client

async def stop_user(user_id):
    client = clients.pop(user_id, None)
    if client:
        await client.stop()

@bot.on_message(filters.command("start"))
async def start(_, message):
    ok = user_id := message.from_user.id
    if not await database.is_authorized(user_id):
        text = f"<blockquote>Soja Bhai tere liye bot nahi bana hai 😂</blockquote>\n\n<blockquote>➤ Developer: {DEVELOPER_USERNAME}</blockquote>"
    else:
        text = f"<blockquote>Kya re jhatu free me kam kr wa raha hai 🤧</blockquote>\n\n<blockquote>➤ Developer: {DEVELOPER_USERNAME}</blockquote>"
    sent = await message.reply_text(text)
    asyncio.create_task(asyncio.sleep(120, result=None))
    async def cleanup():
        await asyncio.sleep(120)
        for msg in (sent, message):
            try: await msg.delete()
            except RPCError: pass
    asyncio.create_task(cleanup())

@bot.on_message(filters.command("help"))
async def help_(_, message):
    await message.reply_text(f"● HOW TO WORK ●\n\n<blockquote expandable>Enable your authorized worker, connect its Telegram session, then run the task worker.</blockquote>\n\n<blockquote>➤ Developer: {DEVELOPER_USERNAME}</blockquote>", parse_mode="html")

@bot.on_message(filters.command("us_me"))
async def authorize(_, message):
    if not owner(message): return
    args = message.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit(): return await message.reply_text("Usage: /us_me <user_id>")
    await database.authorize(int(args[1]))
    await message.reply_text("✅ User authorized.")

@bot.on_message(filters.command("rem_me"))
async def deauthorize(_, message):
    if not owner(message): return
    args = message.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit(): return await message.reply_text("Usage: /rem_me <user_id>")
    await database.deauthorize(int(args[1]))
    await stop_user(int(args[1]))
    await message.reply_text("✅ User access removed.")

@bot.on_message(filters.command("to_me"))
async def users(_, message):
    if not owner(message): return
    ids = await database.list_authorized()
    await message.reply_text("⚡ Current List:\n\n" + "\n".join(f"ID: {x}" for x in ids) if ids else "⚡ Current List:\n\nNo users.")

@bot.on_message(filters.command("taskall"))
async def taskall(_, message):
    global global_tasks
    if not owner(message): return
    arg = message.text.split(maxsplit=1)[-1].lower() if len(message.text.split()) > 1 else ""
    if arg not in {"on", "off"}: return await message.reply_text("Usage: /taskall on|off")
    global_tasks = arg == "on"
    await database.set_global_enabled(global_tasks)
    await message.reply_text(f"✅ Global tasks: {arg.upper()}")

@bot.on_message(filters.command("gen_session"))
async def gen_session(_, message):
    user_id = message.from_user.id
    if not await database.is_authorized(user_id): return
    if await database.get_session(user_id): return await message.reply_text("A session already exists for this account.")
    await message.reply_text("Session generation is ready. Use the configured Pyrogram login flow in a private chat.")

@bot.on_message(filters.command("task"))
async def task(_, message):
    user_id = message.from_user.id
    if not await database.is_authorized(user_id): return
    arg = message.text.split(maxsplit=1)[-1].lower() if len(message.text.split()) > 1 else ""
    if arg not in {"on", "off"}: return await message.reply_text("Usage: /task on|off")
    session = await database.get_session(user_id)
    if arg == "on" and not session: return await message.reply_text("No Telegram session found. Use /gen_session first.")
    if arg == "on":
        await start_user(user_id, session)
    else:
        await stop_user(user_id)
    await message.reply_text(f"✅ Tasks {arg}.")

@bot.on_message(filters.command("status"))
async def status(_, message):
    user_id = message.from_user.id
    mine, glob = await database.stats(user_id)
    uptime = int(asyncio.get_event_loop().time() - started_at)
    await message.reply_text(f"Users: {len(await database.list_authorized())}\n\nUptime: {uptime}s\nPing: N/A\n\nYour Tasks:\n✅ Completed: {mine.get('completed', 0)}\n❌ Filled: {mine.get('filled', 0)}\n\nGlobal:\n✅ Completed: {glob.get('completed', 0)}\n❌ Filled: {glob.get('filled', 0)}")

@bot.on_message(filters.command("restart"))
async def restart(_, message):
    if owner(message):
        await message.reply_text("♻️ Restart requested.")
        raise SystemExit

async def start():
    await bot.start()

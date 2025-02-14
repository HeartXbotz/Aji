from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL
from utils import is_check_admin
import logging  
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("fsub"))
async def force_subscribe(client, message):
    m = await message.reply_text("Wait, I'm checking...")

    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("This command is only for groups!")

    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("Only group admins can use this command!")

    if len(message.command) < 2:
        return await m.edit("Usage: `/fsub CHAT_ID1 CHAT_ID2 ...`")

    toFsub_list = message.command[1:]  # Get all provided chat IDs
    valid_channels = []

    for toFsub in toFsub_list:
        if not toFsub.startswith("-100"):
            toFsub = "-100" + toFsub

        if not toFsub[1:].isdigit() or len(toFsub) != 14:
            return await m.edit(f"Invalid CHAT_ID: `{toFsub}`")

        toFsub = int(toFsub)

        if toFsub == message.chat.id:
            return await m.edit("You cannot set force subscription to the same group!")

        if not await is_check_admin(client, toFsub, client.me.id):
            return await m.edit(f"I need to be an admin in `{toFsub}`! Please make me admin and try again.")

        valid_channels.append(toFsub)

    try:
        await db.setFsub(grpID=message.chat.id, fsubIDs=valid_channels)  # Store list of channels
        return await m.edit(f"✅ Force subscription enabled for `{', '.join(map(str, valid_channels))}` in `{message.chat.title}`!")
    except Exception as e:
        logger.exception(e)
        return await m.edit("⚠️ An error occurred! Please try again or report it in @HeartThieft_bot.")

@Client.on_message(filters.command("del_fsub"))
async def del_force_subscribe(client, message):
    m = await message.reply_text("Wait im checking...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("This command is only for groups!")
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("Only group admins can use this command!")
    ifDeleted =await db.delFsub(message.chat.id)
    if ifDeleted:
        return await m.edit(f"Successfully removed force subscribe for - {message.chat.title}\nTo add again use <code>/fsub YOUR_FSUB_CHAT_ID</code>")
    else:
        return await m.edit(f"Force subscribe not found in {message.chat.title}")

@Client.on_message(filters.command("show_fsub"))
async def show_fsub(client, message):
    m = await message.reply_text("Wait im checking...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("This command is only for groups!")
    # check if commad is given by admin or not
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("Only group admins can use this command!")
    fsub = await db.getFsub(message.chat.id)
    if fsub:
        #now gen a invite link
        invite_link = await client.export_chat_invite_link(fsub)
        await m.edit(f"Force subscribe is set to {fsub}\n<a href={invite_link}>Channel Link Link</a>" ,disable_web_page_preview=True)
    else:
        await m.edit(f"Force subscribe is not set in {message.chat.title}")

from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL
from utils import is_check_admin
import logging  
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("fsub"))
async def force_subscribe(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are anonymous admin. Turn off anonymous admin and try again this command</b>")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>This Command Work Only in group\n\nTry it in your own group</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await client.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    try:
        ids = message.text.split(" ", 1)[1]
        fsub_ids = [int(id) for id in ids.split()]
    except IndexError:
        return await message.reply_text("<b>Command Incomplete!\n\nAdd Multiple Channel By Seperate Space. Like: /fsub id1 id2 id3</b>")
    except ValueError:
        return await message.reply_text('<b>Make Sure Ids are Integer.</b>')        
    channels = "Channels:\n"
    for id in fsub_ids:
        try:
            chat = await client.get_chat(id)
        except Exception as e:
            return await message.reply_text(f"<b>{id} is invalid!\nMake sure this bot admin in that channel.\n\nError - {e}</b>")
        if chat.type != enums.ChatType.CHANNEL:
            return await message.reply_text(f"<b>{id} is not channel.</b>")
        channels += f'{chat.title}\n'
    await save_group_settings(grpid, 'fsub', fsub_ids)
    await message.reply_text(f"<b>Successfully set force channels for {title} to\n\n{channels}\n\nYou can remove it by /nofsub.</b>")
            
    
@Client.on_message(filters.command("del_fsub"))
async def del_force_subscribe(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are anonymous admin. Turn off anonymous admin and try again this command</b>")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>This Command Work Only in group\n\nTry it in your own group</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await client.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    await save_group_settings(grpid, 'fsub', None)
    await message.reply_text(f"<b>Successfully removed force subscribe from {title}.</b>")


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

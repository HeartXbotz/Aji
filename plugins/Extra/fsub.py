from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL
from utils import is_check_admin
import logging  
logger = logging.getLogger(__name__)


# Function to check if a user is an admin in a chat
async def is_check_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]
    except Exception:
        return False  # If an error occurs (e.g., chat not found), assume user is not an admin.

@Client.on_message(filters.command("fsub"))
async def force_subscribe(client, message):
    m = await message.reply_text("Wait, I'm checking...")

    # Ensure the command is used in a group
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("❌ This command is only for groups!")

    # Ensure the user is an admin
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("❌ Only group admins can use this command!")

    # Ensure at least one channel ID is provided
    if len(message.command) < 2:
        return await m.edit("⚠️ Usage: `/fsub CHAT_ID1 CHAT_ID2 ...`\n\nExample: `/fsub -1001234567890 -1009876543210`")

    toFsub_list = message.command[1:]  # Extract provided chat IDs
    valid_channels = []
    invalid_channels = []
    missing_admin_channels = []

    for toFsub in toFsub_list:
        # Ensure the ID starts with "-100" (for channels)
        if not toFsub.startswith("-100"):
            toFsub = "-100" + toFsub

        # Validate ID format
        if not toFsub.lstrip('-').isdigit():
            invalid_channels.append(toFsub)
            continue

        toFsub = int(toFsub)

        # Ensure the group is not setting itself for force-subscription
        if toFsub == message.chat.id:
            return await m.edit("❌ You cannot set force subscription to the same group!")

        # Check if the bot is an admin in the channel
        if not await is_check_admin(client, toFsub, client.me.id):
            missing_admin_channels.append(toFsub)
        else:
            valid_channels.append(toFsub)

    # Report any invalid channel IDs
    if invalid_channels:
        return await m.edit(f"❌ Invalid CHAT_ID(s): `{', '.join(invalid_channels)}`")

    # Report missing admin permissions
    if missing_admin_channels:
        return await m.edit(
            f"⚠️ I need to be an admin in these channels before you can use them for force-subscription:\n\n"
            + "\n".join([f"- `{chat_id}`" for chat_id in missing_admin_channels])
            + "\n\nPlease make me an admin in these channels and try again."
        )

    # Store valid channels in the database
    try:
        await db.setFsub(grpID=message.chat.id, fsubIDs=valid_channels)
        return await m.edit(
            f"✅ Force subscription enabled for `{', '.join(map(str, valid_channels))}` in `{message.chat.title}`!"
        )
    except Exception as e:
        logger.exception(e)
        return await m.edit("⚠️ An error occurred! Please try again or report it in @HeartThieft_bot.")
        

@Client.on_message(filters.command("del_fsub"))
async def del_force_subscribe(client, message):
    m = await message.reply_text("🔍 Checking...")

    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("❌ This command is only for groups!")

    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("❌ Only group admins can use this command!")

    ifDeleted = await db.delFsub(message.chat.id)

    if ifDeleted:
        return await m.edit(
            f"✅ Successfully removed force subscription for **{message.chat.title}**.\n"
            "To add again, use:\n"
            "`/fsub YOUR_FSUB_CHAT_ID`"
        )
    else:
        return await m.edit(f"⚠️ No force subscription found in **{message.chat.title}**.")

@Client.on_message(filters.command("show_fsub"))
async def show_fsub(client, message):
    m = await message.reply_text("🔍 Checking...")

    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("❌ This command is only for groups!")

    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("❌ Only group admins can use this command!")

    fsub_channels = await db.getFsub(message.chat.id)

    if not fsub_channels:
        return await m.edit(f"⚠️ No force subscription is set in **{message.chat.title}**.")

    # Fetch invite links for all channels
    channel_links = []
    for fsub in fsub_channels:
        try:
            chat = await client.get_chat(fsub)
            if chat.username:
                invite_link = f"https://t.me/{chat.username}"
            else:
                invite_link = await client.export_chat_invite_link(fsub)
            channel_links.append(f"🔹 <a href='{invite_link}'>{chat.title}</a>")
        except Exception as e:
            logger.error(f"Error getting invite link for {fsub}: {e}")

    if not channel_links:
        return await m.edit("⚠️ Could not generate invite links for the force-subscription channels.")

    channels_text = "\n".join(channel_links)
    await m.edit(f"✅ **Force Subscription Channels:**\n\n{channels_text}", disable_web_page_preview=True)

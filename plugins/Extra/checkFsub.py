from database.users_chats_db import db
from pyrogram.errors import UserNotParticipant
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import traceback

async def is_user_fsub(bot, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Get the list of force-subscription channels
    fSub_channels = await db.getFsub(chat_id)
    
    if not fSub_channels:  # If no force-subscription is set, allow user
        return True  

    missing_channels = []
    invite_links = []

    for fSub in fSub_channels:
        try:
            # Check if the user is a member of the channel
            await bot.get_chat_member(fSub, user_id)
        except UserNotParticipant:
            try:
                # Try to get the invite link or username-based link
                chat = await bot.get_chat(fSub)
                if chat.username:
                    invite_links.append(f"https://t.me/{chat.username}")
                else:
                    invite_links.append(await bot.export_chat_invite_link(fSub))
                missing_channels.append(chat.title)
            except Exception as e:
                print(f"Error getting invite link for {fSub}: {e}")
                continue

    if not missing_channels:  # If user is in all required channels
        return True

    # Create join buttons for missing channels
    buttons = [InlineKeyboardButton(f"Join {name}", url=link) for name, link in zip(missing_channels, invite_links)]
    keyboard = InlineKeyboardMarkup([buttons])

    # Send warning message
    warning_message = (
        f"<b>⚠️ {message.from_user.mention}, You must join the required channels before sending messages here!</b>"
    )
    k = await message.reply(warning_message, reply_markup=keyboard)

    await message.delete()
    await asyncio.sleep(40)
    await k.delete()
    
    return False

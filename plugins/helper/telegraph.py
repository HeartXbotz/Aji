import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAPH_BOT = "vTelegraphBot"  # Official Telegraph Bot

@Client.on_message(filters.command(["img", "upload"], prefixes="/") & filters.reply)
async def upload_vtelegraph(client, message: Message):
    reply = message.reply_to_message
    user_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if not reply or not reply.media:
        return await message.reply_text("📸 **Reply to an image to upload it to Telegraph.**")

    msg = await message.reply_text("⏳ **Uploading... Please wait.**")

    try:
        # Forward media to @vTelegraphBot and get the forwarded message details
        forwarded_messages = await client.forward_messages(TELEGRAPH_BOT, message.chat.id, reply.id)
        
        # Extract message ID from forwarded message (handling list properly)
        forwarded_message_id = forwarded_messages.id if isinstance(forwarded_messages, Message) else forwarded_messages[0].id

        # Wait for response (Checking every 2 sec for 10 times)
        telegraph_url = None
        for _ in range(10):
            await asyncio.sleep(2)
            async for bot_reply in client.get_chat_history(TELEGRAPH_BOT, limit=5):
                if bot_reply.reply_to_message and bot_reply.reply_to_message.id == forwarded_message_id:
                    if "https://graph.org" in bot_reply.text:
                        telegraph_url = bot_reply.text.strip()
                        break
            if telegraph_url:
                break
        else:
            return await msg.edit_text("❌ **Upload failed. Please try again later.**")

        # Stylish Caption
        caption_text = (
            f"✨ **Image Successfully Uploaded!** ✨\n\n"
            f"👤 **Uploaded by:** {user_mention}\n"
            f"📤 **Hosting:** Telegraph\n"
            f"🔗 **Your Link:** [🔗 View Image]({telegraph_url})\n\n"
            f"⚡ **Share this link with your friends!**\n\n"
            f"🔗 **Powered by:** [Heart Thief](https://t.me/heartthieft)"
        )

        # Inline Buttons
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌍 View Image", url=telegraph_url)],
            [InlineKeyboardButton("🔄 Upload Another", callback_data="upload_another")]
        ])

        # Send Image Preview with Caption
        await message.reply_photo(photo=telegraph_url, caption=caption_text, reply_markup=buttons)

        # Delete "Uploading..." message
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ **Error:** `{str(e)}`")

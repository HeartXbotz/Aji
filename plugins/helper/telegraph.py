import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file  # Telegraph upload library

@Client.on_message(filters.command(["img", "upload", "telegraph"], prefixes="/") & filters.reply)
async def c_upload(client, message: Message):
    reply = message.reply_to_message
    user_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if not reply.photo:
        return await message.reply_text("📸 **Reply to an image to upload it to Telegraph.**")

    msg = await message.reply_text("⏳ **Uploading... Please wait.**")

    try:
        downloaded_media = await reply.download()

        if not downloaded_media:
            return await msg.edit_text("❌ **Download failed. Try again.**")

        # Upload to Telegraph
        telegraph_url = upload_file(downloaded_media)[0]
        file_url = f"https://graph.org{telegraph_url}"
        os.remove(downloaded_media)

        # Stylish Caption
        caption_text = (
            f"✨ **Image Successfully Uploaded!** ✨\n\n"
            f"👤 **Uploaded by:** {user_mention}\n"
            f"🌍 **Host:** Telegraph\n"
            f"🔗 **Direct Link:** [Click to View]({file_url})\n"
            f"⚡ **Share your masterpiece with the world!**\n\n"
            f"🔗 **Powered by:** **[Heart Thief](https://t.me/heartthieft)**\n"
        )

        # Buttons (View Image + Upload Another)
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌍 View Image", url=file_url)],
            [InlineKeyboardButton("🔄 Upload Another", callback_data="upload_another")]
        ])

        # Send Image Preview with Stylish Caption
        await message.reply_photo(photo=file_url, caption=caption_text, reply_markup=buttons)

        # Delete "Uploading..." message
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ **Error:** `{str(e)}`")

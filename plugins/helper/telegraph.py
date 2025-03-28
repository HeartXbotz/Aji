import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file  # Telegraph upload function

@Client.on_message(filters.command(["img", "upload"], prefixes="/") & filters.reply)
async def c_upload(client, message: Message):
    reply = message.reply_to_message
    user_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if not reply.media:
        return await message.reply_text("📸 **Reply to an image to upload it to Telegraph.**")

    msg = await message.reply_text("⏳ **Uploading... Please wait.**")

    try:
        # Download the media
        downloaded_media = await reply.download()

        if not downloaded_media:
            return await msg.edit_text("❌ **Download failed. Try again.**")

        # Upload to Telegraph
        upload_result = upload_file(downloaded_media)  # Returns a list

        if not upload_result:  # If the list is empty, something went wrong
            return await msg.edit_text("❌ **Failed to upload. Try again.**")

        file_url = f"https://graph.org{upload_result[0]}"  # Correct URL format
        os.remove(downloaded_media)  # Remove downloaded file

        # Stylish Caption
        caption_text = (
            f"✨ **Your Image is Ready!** ✨\n\n"
            f"👤 **Uploaded by:** {user_mention}\n"
            f"📤 **Hosting:** Telegraph\n"
            f"🔗 **Your Link:** [🔗 View Image]({file_url})\n\n"
            f"⚡ **Share this link with your friends!**\n\n"
            f"🔗 **Powered by:** [Heart Thief](https://t.me/heartthieft)"
        )

        # Inline Buttons
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌍 View Image", url=file_url)],
            [InlineKeyboardButton("🔄 Upload Another", callback_data="upload_another")]
        ])

        # Send Image Preview with Caption
        await message.reply_photo(photo=file_url, caption=caption_text, reply_markup=buttons)

        # Delete "Uploading..." message
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ **Error:** `{str(e)}`")

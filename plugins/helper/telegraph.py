import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAPH_API_URL = "https://telegra.ph/upload"

@Client.on_message(filters.command(["img", "upload"]) & filters.reply)
async def upload_telegraph(client, message: Message):
    reply = message.reply_to_message
    user_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if not reply or not reply.photo:
        return await message.reply_text("📸 **Reply to an image to upload it to Telegraph.**")

    msg = await message.reply_text("⏳ **Uploading... Please wait.**")
    downloaded_media = None

    try:
        # Download Image
        downloaded_media = await reply.download()
        if not downloaded_media:
            return await msg.edit_text("❌ **Failed to download the image.**")

        # Upload to Telegraph
        with open(downloaded_media, "rb") as f:
            response = requests.post(TELEGRAPH_API_URL, files={"file": f})

        # Handle Response
        if response.status_code != 200:
            return await msg.edit_text(f"❌ **Error: {response.text}**")

        result = response.json()
        if isinstance(result, list) and len(result) > 0 and "src" in result[0]:
            telegraph_url = "https://graph.org" + result[0]["src"]
        else:
            return await msg.edit_text("❌ **Error: Invalid response from Telegraph.**")

        # Caption & Buttons
        caption_text = (
            f"✨ **Image Successfully Uploaded!** ✨\n\n"
            f"👤 **Uploaded by:** {user_mention}\n"
            f"📤 **Hosting:** Telegraph\n"
            f"🔗 **Your Link:** [🔗 View Image]({telegraph_url})\n\n"
            f"⚡ **Share this link with your friends!**\n\n"
            f"🔗 **Powered by:** [Heart Thief](https://t.me/heartthieft)"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌍 View Image", url=telegraph_url)],
            [InlineKeyboardButton("🔄 Upload Another", callback_data="upload_another")]
        ])

        # Send Image Preview
        await message.reply_photo(photo=telegraph_url, caption=caption_text, reply_markup=buttons)
        await msg.delete()

    except requests.exceptions.RequestException as req_err:
        await msg.edit_text(f"❌ **Network Error:** `{req_err}`")
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** `{str(e)}`")
    finally:
        # Ensure the file is deleted even if an error occurs
        if downloaded_media and os.path.exists(downloaded_media):
            os.remove(downloaded_media)

# Callback Handler for "Upload Another"
@Client.on_callback_query(filters.regex("upload_another"))
async def upload_another_callback(client, callback_query):
    await callback_query.message.reply_text("📸 **Reply to an image to upload it to Telegraph.**")

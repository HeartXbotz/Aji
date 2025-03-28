import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

CATBOX_API = "https://catbox.moe/user/api.php"
CUSTOM_DOMAIN = "https://Heartxbotz"  # Your custom domain
DELETE_TIME = 1800  # 30 minutes (in seconds)

@Client.on_message(filters.command(["img", "cup", "catbox"]) & filters.reply)
async def upload_catbox(client, message: Message):
    reply = message.reply_to_message
    user_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if not reply.media:
        return await message.reply_text("Reply to an image, video, or audio file (max 200MB) to upload to Catbox.")

    msg = await message.reply_text("⏳ Uploading... Please wait.")

    try:
        downloaded_media = await reply.download()

        with open(downloaded_media, "rb") as f:
            response = requests.post(CATBOX_API, data={"reqtype": "fileupload"}, files={"fileToUpload": f})

        os.remove(downloaded_media)

        if response.status_code == 200:
            catbox_url = response.text.strip()
            file_name = catbox_url.split("/")[-1]  # Extract file name
            custom_url = f"{CUSTOM_DOMAIN}/{file_name}"  # Custom domain link

            caption_text = (
                f"✨ **File Successfully Uploaded!** ✨\n\n"
                f"👤 **Uploaded by:** {user_mention}\n"
                f"📤 **Hosting:** Catbox\n"
                f"🔗 **Your Link:** [🔗 View File]({catbox_url})\n"
                f"🔗 **Custom Link:** [🔗 {CUSTOM_DOMAIN}]({custom_url})\n\n"
                f"⚡ **Share this link with your friends!**\n\n"
                f"🔗 **Powered by:** [Heart Thief](https://t.me/heartthieft)"
            )

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🐱 View File", url=catbox_url)],
                [InlineKeyboardButton("🔗 Custom Link", url=custom_url)],
                [InlineKeyboardButton("🔄 Upload Another", callback_data="upload_another")]
            ])

            # Send message with preview for images & videos
            if reply.photo:
                sent_msg = await message.reply_photo(photo=catbox_url, caption=caption_text, reply_markup=buttons)
            elif reply.video:
                sent_msg = await message.reply_video(video=catbox_url, caption=caption_text, reply_markup=buttons)
            else:
                sent_msg = await message.reply_text(caption_text, reply_markup=buttons)

            await msg.delete()

            # Auto-delete after 30 minutes
            await asyncio.sleep(DELETE_TIME)
            await sent_msg.delete()

        else:
            await msg.edit_text("❌ Upload failed. Try again later.")

    except Exception as e:
        await msg.edit_text(f"❌ Error: `{str(e)}`")

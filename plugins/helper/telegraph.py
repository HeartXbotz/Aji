import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

CATBOX_API = "https://catbox.moe/user/api.php"

@Client.on_message(filters.command(["img", "cup", "catbox"], prefixes="/") & filters.reply)
async def c_upload(client, message: Message):
    reply = message.reply_to_message

    if not reply.media:
        return await message.reply_text("Reply to an image, video, or audio file (max 200MB) to upload to Catbox.")

    if reply.document and reply.document.file_size > 200 * 1024 * 1024:
        return await message.reply_text("File size limit is 200MB for Catbox.")

    msg = await message.reply_text("Uploading to Catbox...")

    try:
        downloaded_media = await reply.download()

        if not downloaded_media:
            return await msg.edit_text("Something went wrong during download.")

        with open(downloaded_media, "rb") as f:
            response = requests.post(CATBOX_API, data={"reqtype": "fileupload"}, files={"fileToUpload": f})

        if response.status_code == 200:
            await msg.edit_text(f"Uploaded Successfully:\n🔗 `{response.text}`")
        else:
            await msg.edit_text("Upload failed. Try again later.")

        os.remove(downloaded_media)

    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")

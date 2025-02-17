import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import API_ID, API_HASH, BOT_TOKEN  # Import API details from info.py

# List of multiple channel IDs where the bot should add buttons
CHANNEL_IDS = [-1002494713645, -1002181741528, -1002210542830, -1002297980917, -1001673914930, -1002137764926]  # Add more if needed

@Client.on_message(filters.chat(CHANNEL_IDS) & filters.photo)
async def add_button(client, message):
    if message.chat.id in CHANNEL_IDS:
        button = InlineKeyboardMarkup(
            [
             [InlineKeyboardButton("💫 Mᴏᴠɪᴇꜱ Sᴇᴀʀᴄʜ Gʀᴏᴜᴘ 💫", url="https://t.me/TG_Moviesearch")],
             [InlineKeyboardButton("⚜️ Uᴘᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ ⚜️", url="https://t.me/TamizhFiles")]
            ]
        )

        try:
            await message.edit_reply_markup(reply_markup=button)
            await asyncio.sleep(0.5)  # Prevent rate-limit issues
        except Exception as e:
            print(f"Failed to add button: {e}")

#-------------------------- Re-Post Codes ------------------------#
     #   try:
            # Download the media
         #   file_path = await message.download()
        #    if not file_path:
            #    print("Error: Failed to download media.")
          #      return

            # Repost media with buttons
         #   if message.photo:
            #    await client.send_photo(message.chat.id, file_path, caption=message.caption or "", reply_markup=button)
           # elif message.video:
               # await client.send_video(message.chat.id, file_path, caption=message.caption or "", reply_markup=button)
           # elif message.document:
               # await client.send_document(message.chat.id, file_path, caption=message.caption or "", reply_markup=button)

            # Delete the original message (bot must have admin rights)
       #     try:
                #await message.delete()
            #except Exception as e:
              #  print(f"Warning: Could not delete message - {e}")

            # Prevent rate-limiting
            #await asyncio.sleep(0.5)

      #  except Exception as e:
        #    print(f"Failed to add button: {e}")

            

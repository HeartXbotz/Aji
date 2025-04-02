from pyrogram import filters, Client
import bs4, requests, re, asyncio
import os, traceback, random
from info import INSTA_CHANNEL as DUMP_GROUP
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
#    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://snapinsta.app",
    "Connection": "keep-alive",
    "Referer": "https://snapinsta.app/es",
}
@Client.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    global headers
    try:
        m = await message.reply_sticker("CAACAgQAAxkBAAItjWdLyDqMXQaKX0vVcnlK8eEmTQ3XAAKsFgACL3yZUB2upzgClfImHgQ")
        url= link.replace("instagram.com","ddinstagram.com")
        url=url.replace("==","%3D%3D")
        if url.endswith("="):
           dump_file=await message.reply_video(url[:-1],caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
        else:
            dump_file=await message.reply_video(url,caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
        if 'dump_file' in locals():
           await dump_file.forward(DUMP_GROUP)
        await m.delete()
    except Exception as e:
        try:
            if "/reel/" in url:
               ddinsta=True 
               getdata = requests.get(url).text
               soup = bs4.BeautifulSoup(getdata, 'html.parser')
               meta_tag = soup.find('meta', attrs={'property': 'og:video'})
               try:
                  content_value =f"https://ddinstagram.com{meta_tag['content']}"
               except:
                   pass 
               if not meta_tag:
                  ddinsta=False
                  meta_tag = requests.post("https://snapinsta.app/action.php", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
             
                  if meta_tag.ok:
                     res=meta_tag.json()
               
                #     await message.reply(res)
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                     content_value = meta[0]
                  else:
                      return await message.reply("oops something went wrong")
               try:
                   if ddinsta:
                      dump_file=await message.reply_video(content_value,caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
                   else:
                       dump_file=await message.reply_video(content_value, caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
               except:
                   downfile=f"{os.getcwd()}/{random.randint(1,10000000)}"
                   with open(downfile,'wb') as x:
                       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                       x.write(requests.get(content_value,headers=headers).content)
                   dump_file=await message.reply_video(downfile,caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot") 
            elif "/p/" in url:
                  meta_tag = requests.post("https://snapinsta.app/action.php", data = {"q": "link", "t": "media", "lang": "en"}, headers = {"User-Agent": "YourUserAgentHere"})
                  if meta_tag.ok:
                     res=meta_tag.json()
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                  else:
                      return await message.reply("oops something went wrong")
              #    await message.reply(meta)
                  for i in range(len(meta) - 1):
                     com=await message.reply_text(meta[i])
                     await asyncio.sleep(1)
                     try:
                        dump_file=await message.reply_video(com.text,caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
                        await com.delete()
                     except:
                         pass 
            elif "stories" in url:
                  meta_tag = requests.post("https://snapinsta.app/action.php", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                  if meta_tag.ok:
                     res=meta_tag.json()
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                  else:
                      return await message.reply("Oops something went wrong")
                  try:
                     dump_file=await message.reply_video(meta[0], caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
                  except:
                      com=await message.reply(meta[0])
                      await asyncio.sleep(1)
                      try:
                          dump_file=await message.reply_video(com.text,caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Itzheart_bot")
                          await com.delete()
                      except:
                          pass

        except KeyError:
            await message.reply(f"400: Sorry, Unable To Find It Make Sure Its Publically Available :)")
        except Exception as e:
          #  await message.reply_text(f"https://ddinstagram.com{content_value}")
            if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"Instagram {e} {link}")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())
          #     await message.reply(tracemsg)
            ##optinal 
            await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @VeldXd or support chat https://t.me/+DnmZbLjS0iw0YWI1")

        finally:
            if 'dump_file' in locals():
               if DUMP_GROUP:
                  await dump_file.copy(DUMP_GROUP)
            await m.delete()
            if 'downfile' in locals():
                os.remove(downfile)
            await message.reply("<a href='https://t.me/Itzheart_bot'>ᴜsᴇ ɴᴇᴡ ғᴇᴀᴛᴜʀᴇs</a>")


"""

# Headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://snapinsta.app",
    "Connection": "keep-alive",
    "Referer": "https://snapinsta.app/es",
}

@Client.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    """Handles Instagram video download requests."""
    link = message.matches[0].group(0)

    try:
        # Send loading sticker
        m = await message.reply_sticker("CAACAgQAAxkBAAItjWdLyDqMXQaKX0vVcnlK8eEmTQ3XAAKsFgACL3yZUB2upzgClfImHgQ")

        # API URL for Instagram downloader
        api_url = "https://snapinsta.app/action.php"

        # Requesting download URL
        response = requests.post(api_url, data={"q": link, "t": "media", "lang": "en"}, headers=headers)

        if response.ok:
            try:
                res = response.json()
                meta_links = re.findall(r'href="(https?://[^"]+)"', res.get('data', ''))

                if meta_links:
                    for url in meta_links:
                        caption_text = (
                            "✅ **Successfully Downloaded!**\n"
                            "📥 **Downloaded By:** @Itzheart_bot\n"
                            "🔗 **Source:** [Instagram Post]({})".format(link)
                        )
                        dump_file = await message.reply_video(url, caption=caption_text)
                        if DUMP_GROUP:
                            await dump_file.forward(DUMP_GROUP)
                else:
                    await message.reply("⚠️ Sorry, but I couldn't find any downloadable media from that link.")

            except Exception:
                await message.reply("⚠️ Unexpected response. Try again later.")

        else:
            await message.reply("❌ Failed to fetch the media. Please try again in a few moments.")

    except Exception as e:
        # Fallback method using BeautifulSoup
        try:
            getdata = requests.get(link).text
            soup = bs4.BeautifulSoup(getdata, 'html.parser')
            meta_tag = soup.find('meta', attrs={'property': 'og:video'})
            content_value = meta_tag['content'] if meta_tag else None

            if not content_value:
                meta_response = requests.post(api_url, data={"q": link, "t": "media", "lang": "en"}, headers=headers)

                if meta_response.ok:
                    res = meta_response.json()
                    meta_links = re.findall(r'href="(https?://[^"]+)"', res.get('data', ''))
                    content_value = meta_links[0] if meta_links else None

                else:
                    await message.reply("⚠️ Oops, something went wrong while fetching the media.")
                    return

            if content_value:
                caption_text = (
                    "🎬 **Here is your Instagram video!**\n"
                    "✅ **Downloaded By:** @Itzheart_bot\n"
                    "🔗 **Original Post:** [View on Instagram]({})".format(link)
                )
                dump_file = await message.reply_video(content_value, caption=caption_text)
                if DUMP_GROUP:
                    await dump_file.forward(DUMP_GROUP)
            else:
                await message.reply("⚠️ Could not retrieve the video. Try another link.")

        except Exception as e:
            # Logging error to LOG_GROUP if available
            if LOG_GROUP:
                await Mbot.send_message(LOG_GROUP, f"Instagram Error: {e}\nURL: {link}")
                await Mbot.send_message(LOG_GROUP, traceback.format_exc())

            await message.reply(
                "❌ 400: **Sorry, I couldn't find the video.**\n"
                "🔹 Try another link or report the issue to @VeldXd."
            )

    finally:
        # Cleanup
        if 'dump_file' in locals() and DUMP_GROUP:
            await dump_file.copy(DUMP_GROUP)

        await m.delete()
        await message.reply(
            "<a href='https://t.me/Itzheart_bot'>🔹 **Check out my new features!**</a>", 
            disable_web_page_preview=True
        )

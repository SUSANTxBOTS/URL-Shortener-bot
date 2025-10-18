import os
import aiohttp
from pyrogram import Client, filters

API_ID = os.environ.get('21134445')
API_HASH = os.environ.get('231c18ea7273824491d6bf05425ab74e')
BOT_TOKEN = os.environ.get('8462447336:AAGurXMPHtG2fwQSOClkCR-3_HNdXHVi90k')
API_KEY = os.environ.get('73357436b25f2081dec70221ad5dc8f8c579c467')
WEBSITE = os.environ.get('shortloop.site')


try:
    bot = Client('shortener bot',
                 api_id=int(API_ID),
                 api_hash=API_HASH,
                 plugins = dict(root="plugins"),
                 bot_token=BOT_TOKEN,
                 workers=50,
                 sleep_threshold=10)
except Exception:
    print("Add var values properly. Read readme.md once")


@bot.on_message(filters.command('start'))
async def start(bot, message):
    start_msg = f"""
Hi {message.chat.first_name}!

I'm {WEBSITE} bot. Just send me link and get short link!

Send me a link to short a link with random alias.

For custom alias, <code>[link] | [custom_alias]</code>, Send in this format\n
Ex: https://t.me/example | Example

    """
    await message.reply_text(start_msg, disable_web_page_preview=True, quote=True)


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    if "|" in message.text:
        link_parts = message.text.split("|")
        link = link_parts[0]
        aliases = link_parts[1:len(message.text) + 1]
        alias1 = ""
        for alias in aliases:
            alias1 += alias
        x = alias1.replace(" ", "")
    else:
        link = message.matches[0].group(0)
        x= ""
    short_link = await get_shortlink(link, x)
    await message.reply(short_link, quote=True)


async def get_shortlink(link, x):
    url = f'https://{WEBSITE}/api'
    params = {'api': API_KEY,
              'url': link,
              'alias': x
              }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            print(data["status"])
            if data["status"] == "success":
                return f"<code>{data['shortenedUrl']}</code>\n\nHere is your Link:\n{data['shortenedUrl']}"
            else:
                return f"Error: {data['message']}"

bot.run()

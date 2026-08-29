import asyncio
import random
from pathlib import Path

import requests
import telegram
from decouple import config

TG_BOT_TOKEN = config("TG_BOT_TOKEN")
TG_CHANNEL_ID = config("TG_CHANNEL_ID")
FILENAME = "comic_to_send.png"
SECONDS_IN_A_DAY = 86400


async def send_image_to_tg(filename, tg_id, bot, caption):
    with open(filename, "rb") as image:
        await bot.send_photo(chat_id=tg_id, photo=image, caption=caption)


def save_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)


def get_comics_amount():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    return comic_data["num"]


def get_random_comic():
    comics_amount = get_comics_amount()
    comic_number = random.randint(1, comics_amount)
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic_data = response.json()
    return comic_data


async def publish_random_comic(bot):
    comic_data = get_random_comic()
    comic_img_url = comic_data["img"]
    comic_comment = comic_data["alt"]
    save_image(comic_img_url, FILENAME)
    await send_image_to_tg(FILENAME, TG_CHANNEL_ID, bot, comic_comment)
    Path(FILENAME).unlink()


async def publish_comics_daily():
    bot = telegram.Bot(token=TG_BOT_TOKEN)
    while True:
        await publish_random_comic(bot)
        await asyncio.sleep(SECONDS_IN_A_DAY)


def main():
    asyncio.run(publish_comics_daily())


if __name__ == "__main__":
    main()

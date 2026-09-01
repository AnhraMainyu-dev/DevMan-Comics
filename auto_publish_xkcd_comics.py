import random
import time
from pathlib import Path

import requests
from decouple import config

FILENAME = "comic_to_send.png"
SECONDS_IN_A_DAY = 86400


def send_image_to_tg(filename, tg_channel_id, tg_bot_token, caption):
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendPhoto"
    with open(filename, "rb") as image:
        response = requests.post(
            url,
            data={"chat_id": tg_channel_id, "caption": caption},
            files={"photo": image},
        )
    response.raise_for_status()


def save_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)


def get_comics_amount():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    return comic["num"]


def get_random_comic():
    comics_amount = get_comics_amount()
    comic_number = random.randint(1, comics_amount)
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    return comic


def main():
    tg_bot_token = config("TG_BOT_TOKEN")
    tg_channel_id = config("TG_CHANNEL_ID")
    while True:
        comic = get_random_comic()
        save_image(comic["img"], FILENAME)
        try:
            send_image_to_tg(FILENAME, tg_channel_id, tg_bot_token, comic["alt"])
        finally:
            Path(FILENAME).unlink(missing_ok=True)
    time.sleep(SECONDS_IN_A_DAY)


if __name__ == "__main__":
    main()

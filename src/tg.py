#!/usr/bin/python3.8
import urllib, random

from os import makedirs
from os.path import join

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

from src import WaifuGen

API_TOKEN = ""
PIC_DIR = "pics"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply(
        """
Waifu-Generator bot 0.1 is ready to serve


- I WANT WAIFU
    : type it and see what our gacha gonna roll
- /roll easy|medium|hard
    : choose your desiny"""
    )


def _getPic():
    seed = random.randrange(4986277)
    url = f"""https://danbooru.donmai.us/posts/{seed}"""
    out_file = ""
    print(url)
    with urllib.request.urlopen(url) as f:
        src_page = f.read().decode("utf-8")
        splitted_page = src_page.split("picture")
        image_src = splitted_page[1].split('src="')[1].split('">')[0]
        if ".jpg" in image_src:
            image_src = image_src.split(".jpg")[0] + ".jpg"
        elif ".png" in image_src:
            image_src = image_src.split(".png")[0] + ".png"
        print(image_src)
        out_img_name = "image.png" if "png" in image_src else "image.jpg"
        with urllib.request.urlopen(image_src) as response, open(
            out_img_name, "wb"
        ) as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)
        return out_img_name


def _roll(lvl):
    wg = WaifuGen()
    try:
        waifu = "\n".join(wg.roll(level=lvl))
    except:
        try:
            waifu = "\n".join(wg.roll(money=int(lvl)))
        except:
            return (
                join(PIC_DIR, "err.png"),
                "No. We don't serve this. Try to read /help.",
            )
    while True:
        try:
            msg = f""" Here it is, yours only wife:\n\n{waifu} """
            out_img_name = _getPic()
            local_src = join(PIC_DIR, out_img_name)
            return local_src, msg
        except:
            pass


@dp.message_handler(
    commands=[
        "roll",
    ]
)
async def react(message: types.Message):
    local_src, msg = _roll(message.text.split()[1])
    await message.answer_photo(photo=InputFile(local_src), caption=msg)


@dp.message_handler(regexp="I WANT WAIFU")
async def react(message: types.Message):
    local_src, msg = _roll("hard")
    await message.answer_photo(photo=InputFile(local_src), caption=msg)


def run():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    run()

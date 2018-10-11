import asyncio
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

API_TOKEN = '675766688:AAHBDjWDfWDbw9cnQ_8d4lc8cxG-CsY5x_Q'

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def showresults(message):
    address = getpaper(message, 1)

    if address:
        markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=None)
        markup.add(types.InlineKeyboardButton("Click Here to download!", url=address[0]))
        await message.reply("Your paper is ready", reply_markup=markup)
    else:
        address = getpaper(message,2)
        if address:
            markup = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=None)
            markup.add(types.InlineKeyboardButton("Click Here to download!", url=address[0]))
            await message.reply("Your paper is ready", reply_markup=markup)
        else:
            await message.reply("Please send a vilid link of paper's page \n or valid DOI")




@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I am your assistance to get all papers you want!\nsend me link of paper's page or DOI!")


@dp.message_handler()
async def echo(message: types.Message):
    verify=re.search("http",message.text)
    if verify:
        await showresults(message)
    else:
        verify2=re.search("doi.org",message.text)
        if verify2:
            message.text= "http://"+message.text
            await showresults(message)
        else:
            await message.reply("Please send a valid link of paper's page \n or valid DOI")


def getpaper(paper,i):
    if i == 1:
        html_page = urlopen("http://sci-hub.tw/" + paper.text)
    else:
        html_page=urlopen("http://sci-hub.is/"+paper.text)

    soup = BeautifulSoup(html_page)

    for anchor in soup.findAll('div', {'id': 'article'}):
        str_anc = str(anchor)
        # print(str_anc)
        m = re.findall('src="(.+?)#view=FitH', str_anc)
        return m


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True, on_shutdown=shutdown)

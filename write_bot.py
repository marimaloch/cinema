import random
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite3
import requests
from bs4 import BeautifulSoup
import langdetect
import translators

tok_en = '1944577742:AAGRwVD35onQwRb3XaF7B5jcSBbKp970R3Y'
admin_id = '-1001392417350'

database = sqlite3.connect('cinemadb')
sql = database.cursor()
sql.execute("SELECT * FROM links")
cinemadb = sql.fetchall()


scheduler = AsyncIOScheduler()
loop = asyncio.get_event_loop()
bot = Bot(tok_en, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)
photto = 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg'

async def send_admin(dp):
    from aiogram.types import message
    await bot.send_message(chat_id=678168340, text="BOT is working")
    await scheduler_jobs(message)


async def every_five(message):
    bot.send_message(chat_id=678168340, text="Posting/...")
    rand = random.randint(1, len(cinemadb))
    nawe = parser_name(rand)
    disk = parser_diskription(rand)
    pre_lang_geners = parser_genres(rand)

    lwwt = langdetect.detect(nawe)
    post_lang_name = translators.google(nawe, from_language=lwwt, to_language='ru')

    lwwd = langdetect.detect(disk)
    post_lang_disk = translators.sogou(disk, from_language=lwwd, to_language='ru')

    stroke = f'{post_lang_name} \n \n{post_lang_disk} \n #{pre_lang_geners}'
    await bot.send_photo(chat_id=admin_id, photo=parser_photo(rand), caption=stroke)
 #   await bot.send_message(chat_id=admin_id, text=cinemadb[rand])
    sql.execute('DELETE FROM links WHERE link=?', (cinemadb[rand]))
    database.commit()


async def scheduler_jobs(message):
    try:
        scheduler.add_job(every_five, 'cron', hour=9, minute=1, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=12, minute=10, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=16, minute=40, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=19, minute=10, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=22, minute=1, args=(message,))
    except:
        scheduler.add_job(every_five, 'cron', hour=9, minute=5, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=12, minute=15, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=16, minute=45, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=19, minute=15, args=(message,))
        scheduler.add_job(every_five, 'cron', hour=22, minute=5, args=(message,))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="sos")


def parser_name(id):
    f_link = cinemadb[id]
    for i in f_link:
        s_link = i
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'
    }
    req = requests.get(s_link, headers=header)
    soup = BeautifulSoup(req.content, 'html.parser')
    items = soup.find('main', class_='ipc-page-wrapper ipc-page-wrapper--base')
    name = []

    ytems = []

    name.append(items.find('h1', class_='TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG').get_text(strip=True))

    title = name[0]
    return title

def parser_photo(id):
    f_link = cinemadb[id]
    for i in f_link:
        s_link = i
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'
    }
    req = requests.get(s_link, headers=header)
    soup = BeautifulSoup(req.content, 'html.parser')
    items = soup.find('main', class_='ipc-page-wrapper ipc-page-wrapper--base')
    image_href = []
    ytems = []
    image = []

    image_href.append(f"https://www.imdb.com/{items.find('a', class_='ipc-lockup-overlay ipc-focusable').get('href')}")

    images = image_href[0]

    req2 = requests.get(images, headers=header)
    soup2 = BeautifulSoup(req2.content, 'html.parser')
    ytems = soup2.find('main', class_='ipc-page-wrapper ipc-page-wrapper--baseAlt')
    image.append(ytems.find('img', class_='MediaViewerImagestyles__PortraitImage-sc-1qk433p-0 bnaOri').get('src'))

    tit_image = image[0]
    return tit_image

def parser_diskription(id):
    f_link = cinemadb[id]
    for i in f_link:
        s_link = i
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'
    }
    req = requests.get(s_link, headers=header)
    soup = BeautifulSoup(req.content, 'html.parser')
    items = soup.find('main', class_='ipc-page-wrapper ipc-page-wrapper--base')

    diskription = []

    diskription.append(items.find('div', class_='ipc-overflowText ipc-overflowText--pageSection ipc-overflowText--height-long ipc-overflowText--long ipc-overflowText--base').get_text(strip=True))

    a = diskription[0]
    return a

def parser_genres(id):
    f_link = cinemadb[id]
    for i in f_link:
        s_link = i
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'
    }
    req = requests.get(s_link, headers=header)
    soup = BeautifulSoup(req.content, 'html.parser')
    items = soup.find('main', class_='ipc-page-wrapper ipc-page-wrapper--base')
    genre = []

    genre.append(items.find('a', class_='GenresAndPlot__GenreChip-cum89p-3 fzmeux ipc-chip ipc-chip--on-baseAlt').get_text(strip=True))

    genres = genre[0]
    return genres


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, on_startup=send_admin)


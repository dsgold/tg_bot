import asyncio
import os
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, time

from get_weather import get_weather
from voise_transform import textFromVoice

logging.basicConfig(level=logging.INFO)

load_dotenv()

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage)


@dp.message_handler(commands=['погода'])
async def sendWeather(message: types.Message):
    await message.reply(get_weather())


@dp.message_handler(content_types=types.ContentType.VOICE)
async def save_voice_message(message: types.Message):
    file = await bot.get_file(message.voice.file_id)
    file_name = f'voice_messages/v_{message.from_user.full_name}-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.ogg'
    await bot.download_file(file.file_path, file_name)
    result = textFromVoice(path=file_name)
    await message.reply(result)


async def weather():
    w = get_weather()
    await bot.send_message(chat_id=270973023, text='Доброе утро!')
    print('Message received')


async def main():
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(get_weather, 'cron', hour=8, minute=0)
        scheduler.start()

        await dp.start_polling()
    finally:
        scheduler.shutdown()
        await dp.storage.close()
        await dp.storage.wait_closed()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

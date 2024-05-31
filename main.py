import asyncio
import sys
from aiogram import Bot, Dispatcher
import lib;
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.command import CommandObject
from abstract import Provider;
from file import FileProvider;
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import logging

TOKEN = '7387036643:AAFoTl-VVu9kqqhynxxXX0cvUxJjgyiA4f4'

dp = Dispatcher()

provider: Provider = FileProvider('data.txt')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

chatId:int = 0


@dp.message(CommandStart())
async def send_start_message(message: Message) -> None:
  global chatId
  chatId = message.from_user.id
  scheduler = AsyncIOScheduler()
  scheduler.add_job(get_current_actions, 'interval', seconds=60)
  scheduler.start()
  await message.answer('Пришли мне сообщение формата "время - действие" и я запомню его.\n Например: "17:00 - Выключить утюг"')

@dp.message(Command("run"))
async def run(
        message: Message,
        command: CommandObject
):
  now = datetime.datetime.now()
  actions = provider.get_action_on_time_exist(now.hour, now.minute)
  await message.answer(''.join(actions))

@dp.message(Command("clear"))
async def clear(
        message: Message,
        command: CommandObject
):
  provider.clear_data()

@dp.message()
async def get_text_message(message: Message) -> None: 
  if message.text and message.text.find('-') != -1:
    [time, action] = lib.parse_message(message.text)
    await bot.send_message(message.from_user.id, f'Окей, ставлю напоминание: {time} {action}')
    lib.save_action(provider, message.text)

async def send_message(text) -> None:
  global chatId
  if text:
    await bot.send_message(chatId, text)

async def get_current_actions():
  now = datetime.datetime.now()
  actions = provider.get_action_on_time_exist(now.hour, now.minute)
  await send_message(''.join(actions))


async def main() -> None:
  await dp.start_polling(bot)
  

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
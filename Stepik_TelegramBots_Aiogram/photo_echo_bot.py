from aiogram import Bot, Dispatcher
from aiogram.filters import Command  # класс Command нужен, чтобы фильтровать апдейты по наличию в них команд
from aiogram.types import Message  # класс Message - апдейты этого типа мы будем ловить эхо-ботом
from aiogram.types import ContentType # Чтобы наш эхо-бот мог срабатывать на отправку фото
from aiogram import F # Чтобы наш эхо-бот мог срабатывать на отправку фото

with open ('tg_bot.txt', 'r') as f:
    BOT_TOKEN = f.readline()

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)

# Этот хэндлер будет срабатывать на отправку боту стикера
async def send_sticker_echo(message: Message):
    print(message)
    await message.reply_sticker(message.sticker.file_id)


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
# @dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_sticker_echo, F.sticker)
dp.message.register(send_echo)
# То есть мы можем обращаться к полю диспетчера, отвечающего за тип сообщения,
# которое мы хотим обработать хэндлером и вызвать у него метод register,
# а в качестве аргументов передать ему имя хэндлера и фильтры. Регистрировать
# хэндлеры также важно в правильном порядке, чтобы обработчики случайно
# не перехватывали сообщения, которые для них не предназначены.

if __name__ == '__main__':
    dp.run_polling(bot)
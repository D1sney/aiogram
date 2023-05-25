from aiogram import Bot, Dispatcher ,executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import filters      # для IDFilter 
from my_botconfig import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def start(_): # срабатывает когда бот запускается
    print ('bot work')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # resize_keyboard означает сделать клавиатуру локаничной, а one_time_keyboard означает скрывать клавиатуру после каждого сообщения
b1=KeyboardButton('/sticker')
b2=KeyboardButton('/fillle')
kb.add(b1).insert(b2) # add добавляет кнопку в клавиатуру, insert создает новый столбец кнопок и добавляет туда кнопку



# минус IDFilter заключается в том что если вы хотите во время работы бота изменять список пользователей с доступом, то придется сделать проверку id в самой функции, так как хэндлер увидит изменения только после перезапуска скрипта
# IDFilter распознает id пользователя и в виде строкового значения и в виде целочисленного
@dp.message_handler(filters.IDFilter(chat_id='1063427532'), commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Hello', reply_markup=kb) # reply_markup означает вызвать клавиатуру после данного сообщения

@dp.message_handler(commands=['sticker']) # поймать сообщение
async def sticker(message: types.Message):
    await bot.send_message(message.from_user.id, 'look at this🫠', reply_markup=ReplyKeyboardRemove()) # ReplyKeyboardRemove означает удалить клавиатура после этого сообщения
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEH9-lkAAHPeJLG9WWvuvRHsqFIqgaoqX0AAgUBAAL3AsgP0eV0t0YlpKEuBA') # upper это значит преобразовать текст в верхний регистр, capitalize это возвести первую букву текста в верхний регистр
    await message.delete()

@dp.message_handler(commands=['fillle'])
async def file(message: types.Message):
    file = open(r'test.txt', 'r', encoding='utf8')
    x=file.read()
    print(x)
    await message.answer(x)
    file.close()

@dp.message_handler(commands=['photo']) # поймать сообщение
async def photo(message: types.Message):
    await message.reply('This is picture')
    await bot.send_photo(message.chat.id, photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.hindustantimes.com%2Fimg%2F2022%2F11%2F20%2F550x309%2FFh8-GrTWQAMEno8_1668910522750_1668910539398_1668910539398.jpg&imgrefurl=https%3A%2F%2Fwww.hindustantimes.com%2Fsports%2Ffootball%2Fmakes-it-even-more-iconic-fans-work-out-crazy-fifa-world-cup-theory-behind-cristiano-ronaldo-and-lionel-messi-s-internet-breaking-picture-louis-vuitton-101668910397781.html&tbnid=6syC_JHI8YoJcM&vet=10CAgQMyhrahcKEwiY5aXk7tz9AhUAAAAAHQAAAAAQAw..i&docid=tJ6N2gFrEWooRM&w=549&h=309&q=picture&ved=0CAgQMyhrahcKEwiY5aXk7tz9AhUAAAAAHQAAAAAQAw') # upper это значит преобразовать текст в верхний регистр, capitalize это возвести первую букву текста в верхний регистр
    await message.delete()

@dp.message_handler(commands=['location']) # поймать сообщение
async def location(message: types.Message):
    await message.reply('New York')
    await bot.send_location(chat_id=message.from_user.id, latitude=30, longitude=90) # upper это значит преобразовать текст в верхний регистр, capitalize это возвести первую букву текста в верхний регистр
    await message.delete() # message.from_user.id это отправить сообщение в личку тому кто написал, а message.chat.id это отправить в тот чат куда написали

@dp.message_handler(content_types=['sticker'])
async def sticker_id(message: types.Message):
    await message.answer(message.sticker.file_id) 

@dp.message_handler() # поймать сообщение
async def echo(message: types.Message):
    if message.text.count('🥺')>=2:
        await message.answer(message.text.count('🥺'))







if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start, skip_updates=True) # skip_updates игнорирует сообщения отправленные боту до его запуска
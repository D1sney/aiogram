from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import InputFile
from aiogram.utils.callback_data import CallbackData
from my_botconfig import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

START_COMMAND = '''
здарова
'''

HELP_COMMAND = '''
тут помогут
мэйби
'''


# способ 1
# async def get_gif():
#     CATALOG_PHOTO = InputFile(r'C:\Users\ivan3\OneDrive\Рабочий стол\projects\Alex_bot\logoGIF.gif')
#     return CATALOG_PHOTO


# способ через пинтерест (открывается с 'открыть with')
# CATALOG_PHOTO = r'https://i.pinimg.com/236x/51/a5/df/51a5dff8db146ab1b835b627b1b6b65b.jpg'


# способ 2 (остаются не закрытые файлы)
# async def get_gif():
#     CATALOG_PHOTO = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\projects\Alex_bot\logoGIF.gif', 'rb')
#     return CATALOG_PHOTO

# в итоге есть два рабочих способа: первый узнать айди файла, второй просто сохранить путь к файлу в переменную, а уже внутри функции в хэндлере встасить переменную в InputFile


CATALOG_PHOTO = 'CgACAgIAAxkBAAIBsmRQ-kNVVayGCbP8tm0XDob7y7nzAAJSRAACPVOJShVj3NTVcL13LwQ'
# ID гифки с планетой: CgACAgIAAxkBAAIBjmRQ9LkVDJbS3xLVb2xypWBDF67UAAIbRAACPVOJSn72cXp9sxweLwQ
CATALOG_CAPTION = 'Krypto'

# фильтры

KYC = CallbackData('KYC', 'action')


# клавиатуры

kb1=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
b1 = KeyboardButton('Каталог')
b2 = KeyboardButton('Помощь')
kb1.add(b1).add(b2)

KYC_kb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text = 'Binance',
                           callback_data = KYC.new('Binance'))
ib2 = InlineKeyboardButton(text = 'ByBit',
                           callback_data = KYC.new('ByBit'))
ib3 = InlineKeyboardButton(text = 'OKX',
                           callback_data = KYC.new('OKX'))
ib4 = InlineKeyboardButton(text = 'Huobi',
                           callback_data = KYC.new('Huobi'))
ib5 = InlineKeyboardButton(text = 'Bit Get',
                           callback_data = KYC.new('Bit Get'))
ib6 = InlineKeyboardButton(text = 'Coinbase',
                           callback_data = KYC.new('Coinbase'))
ib7 = InlineKeyboardButton(text = 'Binance US',
                           callback_data = KYC.new('Binance US'))
ib8 = InlineKeyboardButton(text = 'Kucoin',
                           callback_data = KYC.new('Kucoin'))
KYC_kb.add(ib1, ib7, ib3, ib4, ib5, ib6, ib2, ib8)

ikb2 = InlineKeyboardMarkup(row_width=2)
ib2_1 = InlineKeyboardButton(text = 'купить',
                           callback_data = 'buy')
ib2_2 = InlineKeyboardButton(text = 'вернуться',
                           callback_data = 'home')
ikb2.add(ib2_1, ib2_2)

ikb3 = InlineKeyboardMarkup(row_width=2)
ib3_1 = InlineKeyboardButton(text = 'вернуться',
                           callback_data = 'home2')
ikb3.add(ib3_1)

# главные команды

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, START_COMMAND, reply_markup=kb1)

##############################################################
@dp.message_handler (content_types=types.ContentType.ANIMATION)
async def send_photo_file_id(message: types.Message):
    await message.reply(message.animation.file_id)
##############################################################

@dp.message_handler(text = 'Помощь')
async def help_command(message: types.Message):
    await message.delete()
    await bot.send_message(message.chat.id, HELP_COMMAND)

@dp.message_handler(text = 'Каталог')
async def catalog_command(message: types.Message):    
    await bot.send_animation(message.chat.id, animation=CATALOG_PHOTO, caption=CATALOG_CAPTION, reply_markup=kb1)    
# калбэки


@dp.callback_query_handler(KYC.filter(action='Binance'))
async def binance_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass1'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def bybit_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='animation', caption='pass2'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def okx_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass3'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def huobi_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass4'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def bitget_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass5'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def coinbase_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass6'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def binanceus_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass7'), reply_markup=ikb2)

@dp.callback_query_handler(KYC.filter(action='Binance'))
async def Kucoin_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='photo', caption='pass8'), reply_markup=ikb2)






@dp.callback_query_handler(text='home')
async def home_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='animation', caption=CATALOG_CAPTION), reply_markup=kb1)
    await callback.answer('Вы вернулись в каталог')

@dp.callback_query_handler(text='buy')
async def home_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='animation', caption='Выберите количество'), reply_markup=ikb3)
    await callback.answer('Вы вернулись в каталог')






@dp.callback_query_handler(text='home2')
async def home_command(callback: types.CallbackQuery):
    await callback.message.edit_media(types.InputMedia(media=CATALOG_PHOTO, type='animation', caption=CATALOG_CAPTION), reply_markup=kb1)
    await callback.answer('Вы вернулись в каталог')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
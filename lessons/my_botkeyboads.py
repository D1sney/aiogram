from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

kb=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1=KeyboardButton('/help')
b2=KeyboardButton('/photo')
b3=KeyboardButton('/sticker')
kb.add(b1,b2,b3)

ikb=InlineKeyboardMarkup(row_width=2)
ib1=InlineKeyboardButton('❤️',
                         callback_data='like')
ib2=InlineKeyboardButton('💔',
                         callback_data='dislike')
ib3=InlineKeyboardButton('next photo',
                         callback_data='nextphoto')
ikb.add(ib1,ib2,ib3)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

ikb=InlineKeyboardMarkup(row_width=3)
ib1=InlineKeyboardButton('❤️',
                         callback_data='like')
ib2=InlineKeyboardButton('💔',
                         callback_data='dislike')
ib3=InlineKeyboardButton('next photo',
                         callback_data='nextphoto')
ib4=InlineKeyboardButton('minion',
                         callback_data='minion')
ib5 = InlineKeyboardButton('change photo',
                           callback_data='changephoto')
ib6 = InlineKeyboardButton('boom',
                           callback_data='boom')
ikb.add(ib1,ib2).add(ib3,ib4,ib5).add(ib6)

kb1=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1=KeyboardButton('Photos')
b2=KeyboardButton('/hello')
kb1.add(b1,b2)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
kb=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('🐳')
b3 = KeyboardButton('/random_place')
kb.add(b1,b3)

kb2=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b2 = KeyboardButton('/orange')
kb2.add(b2)

ikb = InlineKeyboardMarkup(row_width=4)
ib1 = InlineKeyboardButton(text = 'Typing club',
                        #    url = 'https://www.typingclub.com/sportal/program-3/353.play',
                           callback_data='typingclub')
ib2 = InlineKeyboardButton(text = 'Tele API',
                           url = 'https://core.telegram.org/bots/api#replykeyboardremove')
ikb.add(ib1,ib2)
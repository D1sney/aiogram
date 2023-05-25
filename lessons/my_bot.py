from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from my_botkeyboads import ikb, kb
from my_botconfig import TOKEN_API
import random , os

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def start(_):
    print('work it work it')

START_COMMAND ='''
/help - описание всех команд
/photo - рандомное фото
/sticker - рандомный стикер
'''
photos = ['https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.hindustantimes.com%2Fimg%2F2022%2F11%2F20%2F550x309%2FFh8-GrTWQAMEno8_1668910522750_1668910539398_1668910539398.jpg&imgrefurl=https%3A%2F%2Fwww.hindustantimes.com%2Fsports%2Ffootball%2Fmakes-it-even-more-iconic-fans-work-out-crazy-fifa-world-cup-theory-behind-cristiano-ronaldo-and-lionel-messi-s-internet-breaking-picture-louis-vuitton-101668910397781.html&tbnid=6syC_JHI8YoJcM&vet=10CAgQMyhrahcKEwiY5aXk7tz9AhUAAAAAHQAAAAAQAw..i&docid=tJ6N2gFrEWooRM&w=549&h=309&q=picture&ved=0CAgQMyhrahcKEwiY5aXk7tz9AhUAAAAAHQAAAAAQAw',
          'https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F4%2F43%2FAmbersweet_oranges.jpg&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FOrange_(word)&tbnid=bd487gs314KMhM&vet=12ahUKEwieqtD_it_9AhUQsSoKHY1QBfQQMygKegUIARDWAQ..i&docid=lOUrMhsJMwmW1M&w=1999&h=2254&q=orange&ved=2ahUKEwieqtD_it_9AhUQsSoKHY1QBfQQMygKegUIARDWAQ',
          'https://www.google.com/imgres?imgurl=https%3A%2F%2Fmedia.npr.org%2Fassets%2Fimg%2F2014%2F08%2F07%2Fmonkey-selfie_custom-7117031c832fc3607ee5b26b9d5b03d10a1deaca-s1100-c50.jpg&tbnid=NVCBiDkk1LhYRM&vet=12ahUKEwi-96G0k-T9AhWTwioKHf_PB8IQMygQegUIARDdAQ..i&imgrefurl=https%3A%2F%2Fwww.npr.org%2Fsections%2Fthetwo-way%2F2014%2F08%2F07%2F338668652%2Fif-a-monkey-takes-a-photo-who-owns-the-copyright&docid=c5YxPV3AvUajLM&w=1085&h=1500&q=photo&ved=2ahUKEwi-96G0k-T9AhWTwioKHf_PB8IQMygQegUIARDdAQ']
descriptions = ['SIUUUUUUU', 'Orange, 100k like g00d', 'Monkey king love fruits!!!\nBut this is common vegetable monkey']
stickers = ['CAACAgIAAxkBAAEH9-lkAAHPeJLG9WWvuvRHsqFIqgaoqX0AAgUBAAL3AsgP0eV0t0YlpKEuBA',
            'CAACAgIAAxkBAAICVmQSTU05eKzPgE8LI3V8BnAlbOfBAAJiAANOXNIpTqLDGEjEK3EvBA',
            'CAACAgIAAxkBAAIDBmQU_LDAp7p0Cgmeztq7DGkCub_dAAIzAQAC5KDOBw7XijNrJm0NLwQ',
            'CAACAgIAAxkBAAIDCGQU_NObBslt2YKiisNh87d2dD0tAAIoDwACGRboSeGR09uL53XbLwQ']
status = ['','','']
choice = ''

@dp.message_handler(commands=['start', 'help'])
async def help_command(message: types.Message):
    await message.answer(START_COMMAND,
                         reply_markup=kb)
    await message.delete()

@dp.message_handler(commands=['photo'])
async def photo_command(message: types.Message):
    global choice
    choice = random.randrange(0, len(photos))
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photos[choice],
                         caption=descriptions[choice],
                         reply_markup=ikb)


@dp.callback_query_handler()
async def callback_command(callback: types.CallbackQuery):
    global status
    if callback.data == 'like' and status[choice] != 'like':
        status[choice] = 'like'
        await callback.answer(text='like')
    if callback.data == 'like' and status[choice] == 'like':
        await callback.answer(text='Вы уже лайкали это фото')
    if callback.data == 'dislike' and status[choice] != 'dislike':
        status[choice] = 'dislike'
        await callback.answer(text='Удалим из ваших рекомендаций')
    if callback.data == 'dislike' and status[choice] == 'dislike':
        await callback.answer(text='уже давно удалено из рекомендаций')
    











@dp.message_handler(commands=['sticker'])
async def sticker_command(message: types.Message):
    await bot.send_sticker(chat_id= message.from_user.id, sticker=random.choice(stickers))
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start)
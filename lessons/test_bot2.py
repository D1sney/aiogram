from aiogram import Bot, Dispatcher, executor, types
import random, asyncio, time
from aiogram.dispatcher.filters import Text
from test_bot2keyboards import kb,kb2,ikb
from my_botconfig import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def start(_):
    print('test_bot2 was start')


@dp.message_handler(commands=['random_place'])
async def place_command(message: types.Message):
    await bot.send_location(chat_id=message.chat.id,
                            latitude=random.randint(-90,90), longitude=random.randint(-180,180))

@dp.message_handler(commands=['start2'])
async def start_command2(message: types.Message):
    await asyncio.sleep(1)
    await message.answer( 'Hello2', reply_markup=kb2)

@dp.message_handler(commands=['orange'])
async def orange_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, 
                         photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F4%2F43%2FAmbersweet_oranges.jpg&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FOrange_(word)&tbnid=bd487gs314KMhM&vet=12ahUKEwieqtD_it_9AhUQsSoKHY1QBfQQMygKegUIARDWAQ..i&docid=lOUrMhsJMwmW1M&w=1999&h=2254&q=orange&ved=2ahUKEwieqtD_it_9AhUQsSoKHY1QBfQQMygKegUIARDWAQ', 
                         caption='Choose faster',
                         reply_markup=ikb)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    time.sleep(5)                                                               # когда ты пишешь time.sleep, а не asyncio.sleep, весь скрипт ждет исполнения этой команды и другие команды исполняются не конкурентно
    await asyncio.sleep(3)                                                      # но после обычного time.sleep, asyncio.sleep конкурирует с другими asyncio.sleep, а конкретно с asyncio.sleep в функции start2   и если запустить эти две функции одновременно(сначала start1), то в этом эксперименте start2 отправит сообщение раньше
    await bot.send_message(message.from_user.id, 'Hello', reply_markup=kb)      # а если прервать исполнение start2 и отправить start1, то исполнение кода перейдет на start1 и весь скрипт будет ждать пока не исполнится time.sleep(5), а уже потом будет конкуренция между продолжением start1 и start2

@dp.message_handler(Text(equals='Elephant'))
async def elephant_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Elephantik🐘') 


@dp.message_handler()
async def sticker_command(message: types.Message):
    if message.text == '🐳':
        await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAICVmQSTU05eKzPgE8LI3V8BnAlbOfBAAJiAANOXNIpTqLDGEjEK3EvBA')
    elif '✌🏼' in message.text:
        await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAICVmQSTU05eKzPgE8LI3V8BnAlbOfBAAJiAANOXNIpTqLDGEjEK3EvBA')

@dp.callback_query_handler()
async def calbak(callback: types.CallbackQuery):
    if callback.data == 'typingclub':
        await callback.answer(text='typing club good') 



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start, skip_updates=True)

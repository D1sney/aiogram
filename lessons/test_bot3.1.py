from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import Text
import random
from test_bot3keyboards import ikb
from my_botconfig import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def start(_):
    print('Let`s go')

async def send_random(message: types.Message):
    random_photo = random.choice(list(photos.keys()))
    await bot.send_photo(message.chat.id, # если поставить message.from_user.id то будет ошибка что бот не может отправлять сообщнгие боту (самому себе в данном случае)
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)   



arr_photos = ['https://www.google.com/imgres?imgurl=http%3A%2F%2Fwww.radionetplus.ru%2Fuploads%2Fposts%2F2013-12%2F1387478876_krasivye-fotki-1.jpeg&tbnid=vRB6qLSvKbRboM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygEegUIARDYAQ..i&imgrefurl=http%3A%2F%2Fwww.radionetplus.ru%2Fizobrazhenija%2Fkrasivye_kartinki%2F46023-foto-assorti-krasivye-fotki-25-fotografiy.html&docid=JmDCp60NupPyWM&w=600&h=399&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygEegUIARDYAQ',
              'https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.meme-arsenal.com%2Fmemes%2F9c3e5768b4273ebd998ef4a425f4a875.jpg&tbnid=xTE40kG8oAYdWM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygMegUIARDoAQ..i&imgrefurl=https%3A%2F%2Fwww.meme-arsenal.com%2Fcreate%2Fchose%3Ftag%3D%25D0%25BA%25D1%2580%25D1%2583%25D1%2582%25D1%258B%25D0%25B5%2520%25D1%2584%25D0%25BE%25D1%2582%25D0%25BA%25D0%25B8&docid=AYkIZa098iBX8M&w=224&h=300&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygMegUIARDoAQ',
              'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimage1.thematicnews.com%2Fuploads%2Fimages%2F00%2F00%2F39%2F2020%2F09%2F29%2Fed9822cc6a.jpg&tbnid=3oBZn2wiVYC_vM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygtegUIARCqAg..i&imgrefurl=https%3A%2F%2Fmyprikol.com%2F2020%2F09%2Fsmeshnye-kartinki-i-fotki_4.html&docid=EeCQ2AuBAjKJiM&w=640&h=682&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygtegUIARCqAg']

captions = ['Cristmas cat', 'Abibas', 'IT']

photos = dict(zip(arr_photos, captions))








@dp.message_handler(Text(equals='Photos'))
async def photos_command(message: types.Message):
    await send_random(message)


@dp.callback_query_handler()
async def photo_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer('YOu L1ke Th1s Phot0')
    if callback.data == 'dislike':
        await callback.message.answer('You dont like this photo')
        await callback.answer('fuuuuuuuu')
    if callback.data == 'minion':
        await bot.send_photo(chat_id=callback.message.chat.id, # inline клавиатура может отправлять все тоже самое что и бот только надо обращаться к нему через callback
                             photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Ftipik.ru%2Fwp-content%2Fuploads%2F2019%2F09%2F%25D0%259F%25D1%2580%25D0%25B8%25D0%25BA%25D0%25BE%25D0%25BB%25D1%258C%25D0%25BD%25D1%258B%25D0%25B5-%25D1%2584%25D0%25BE%25D1%2582%25D0%25BA%25D0%25B8-%25D0%25BD%25D0%25B0-%25D0%25B0%25D0%25B2%25D0%25B0%25D1%2582%25D0%25B0%25D1%2580%25D0%25BA%25D1%2583-003.jpg&tbnid=C8_OMrRKc_4DSM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMyhRegUIARCmAQ..i&imgrefurl=https%3A%2F%2Ftipik.ru%2Fprikolnye-fotki-na-avatarku%2F&docid=4nYu9kQSBemMeM&w=400&h=587&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMyhRegUIARCmAQ')
        await callback.answer()
    if callback.data == 'nextphoto':
        await send_random(message=callback.message)
        await callback.answer()
        









if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start)
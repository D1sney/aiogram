from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import Text
import random
from test_bot3keyboards import ikb, kb1, ReplyKeyboardRemove
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InputContactMessageContent     # тема Inline режим
import uuid
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from my_botconfig import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def start(_):
    print('Let`s go')

arr_photos = ['https://www.google.com/imgres?imgurl=http%3A%2F%2Fwww.radionetplus.ru%2Fuploads%2Fposts%2F2013-12%2F1387478876_krasivye-fotki-1.jpeg&tbnid=vRB6qLSvKbRboM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygEegUIARDYAQ..i&imgrefurl=http%3A%2F%2Fwww.radionetplus.ru%2Fizobrazhenija%2Fkrasivye_kartinki%2F46023-foto-assorti-krasivye-fotki-25-fotografiy.html&docid=JmDCp60NupPyWM&w=600&h=399&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygEegUIARDYAQ',
              'https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.meme-arsenal.com%2Fmemes%2F9c3e5768b4273ebd998ef4a425f4a875.jpg&tbnid=xTE40kG8oAYdWM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygMegUIARDoAQ..i&imgrefurl=https%3A%2F%2Fwww.meme-arsenal.com%2Fcreate%2Fchose%3Ftag%3D%25D0%25BA%25D1%2580%25D1%2583%25D1%2582%25D1%258B%25D0%25B5%2520%25D1%2584%25D0%25BE%25D1%2582%25D0%25BA%25D0%25B8&docid=AYkIZa098iBX8M&w=224&h=300&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygMegUIARDoAQ',
              'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimage1.thematicnews.com%2Fuploads%2Fimages%2F00%2F00%2F39%2F2020%2F09%2F29%2Fed9822cc6a.jpg&tbnid=3oBZn2wiVYC_vM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygtegUIARCqAg..i&imgrefurl=https%3A%2F%2Fmyprikol.com%2F2020%2F09%2Fsmeshnye-kartinki-i-fotki_4.html&docid=EeCQ2AuBAjKJiM&w=640&h=682&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMygtegUIARCqAg']
captions = ['Cristmas cat', 'Abibas', 'IT']

photos = dict(zip(arr_photos, captions))
random_photo = random.choice(list(photos.keys()))

flag = True


# pre-process update 
# process update
# pre-process message |callback_query
# filter (lambda message: not message.photo)
# process message|callback_query|...et cetera
# handler
# post process message
# post process update

ADMIN = 1063427532

class AdminMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message.from_user.id != ADMIN:
            raise CancelHandler()           # если id пользователя не прошел проверку то вызывается исключение которое блокирует далее отправление update к хэндлерам и следующим поочереди Middleware

class Test2Middleware(BaseMiddleware):
    
    async def on_pre_process_message(self, update: types.Update, data: dict):       
        print('2on_pre_process_message')
    async def on_process_message(self, message: types.Message, data: dict):
        print('2process_message')
    

class TestMiddleware(BaseMiddleware):           # если в одном классе несколько функций с одинаковыми названиями, то исполняется только та которая написана ниже, но можно зарегестрировать два класса внутри которых будут одноименные функции, первая из них исполнится та, чей класс раньше зарегистрирован

    async def on_pre_process_update(self, update: types.Update, data: dict):        # обязательно именно такое название функции, при другом название ничего не будет работать и так же обязательны именно такие же аргументы
        print('2on_pre_process_update')
    async def on_pre_process_update(self, update: types.Update, data: dict):        
        print('on_pre_process_update')
    async def on_process_update(self, update: types.Update, data: dict):        # порядок выполнения функций в Middleware зависит не от их порядка а от их названия, существует порядок названия функций который надо соблюдать 
        print('on_process_update')
    async def on_pre_process_message(self, update: types.Update, data: dict):       # важно в название функции не забывать в начале добавлять on_
        print('on_pre_process_message')
    async def on_process_message(self, message: types.Message, data: dict):
        print('process_message')
    async def on_process_update(self, update: types.Update, data: dict):        
        print('2on_process_update')

    async def on_post_process_message(self, message: types.Message, data_check: list, data: dict):    # в два последних middleware надо передать аргумент в данном случае который называется data_check, этот аргумент хранит в себе данные которые мы передавали из предыдущих middleware 
        print('post_process_message')
    async def on_post_process_update(self, update: types.Update, data_check: list, data: dict):
        print('post_process_update')



@dp.message_handler(commands=['hello', 'start'])
async def edit_command(message: types.Message):
    await message.answer('Hellooo',
                         reply_markup=kb1)
    print('World')
    # await message.edit_media(types.InputMedia(media=''))  # бот не может редактировать сообщения пользователя

@dp.message_handler(Text(equals='Photos'))
async def photos_command(message: types.Message):
    global random_photo
    random_photo = random.choice(list(photos.keys()))   # если использовать только эту строчку то в changephoto при нажтии на эту кнопку иногда будет происходить исключение, а если не использовать вообще то при отправки боту текста Photos, бот всегда будет присылать аналогичную фотографию тк random_photo не изменяется с каждым вызовом этой функции
    await bot.send_photo(message.from_user.id,
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)

@dp.callback_query_handler()
async def photo_callback(callback: types.CallbackQuery):
    global random_photo # мы объявили глобальную переменную чтобы в changephoto можно было исключить фотку которую мы хотим изменить 
    global flag
    if callback.data == 'like':
        if flag:
            await callback.answer('YOu L1ke Th1s Phot0')
            flag = not flag
        else:
            await callback.answer('You уже likали эту фоточку')

    if callback.data == 'dislike':
        await callback.message.answer('You dont like this photo')
        await callback.message.delete()
        await callback.answer('fuuuuuuuu')
    if callback.data == 'minion':
        await bot.send_message(chat_id=callback.message.chat.id,
                               text='Ydalenie клавиатуры',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Ftipik.ru%2Fwp-content%2Fuploads%2F2019%2F09%2F%25D0%259F%25D1%2580%25D0%25B8%25D0%25BA%25D0%25BE%25D0%25BB%25D1%258C%25D0%25BD%25D1%258B%25D0%25B5-%25D1%2584%25D0%25BE%25D1%2582%25D0%25BA%25D0%25B8-%25D0%25BD%25D0%25B0-%25D0%25B0%25D0%25B2%25D0%25B0%25D1%2582%25D0%25B0%25D1%2580%25D0%25BA%25D1%2583-003.jpg&tbnid=C8_OMrRKc_4DSM&vet=12ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMyhRegUIARCmAQ..i&imgrefurl=https%3A%2F%2Ftipik.ru%2Fprikolnye-fotki-na-avatarku%2F&docid=4nYu9kQSBemMeM&w=400&h=587&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=2ahUKEwja3bv5lfP9AhWCuioKHZOBDKsQMyhRegUIARCmAQ',
                             reply_markup=ikb)
        await callback.message.delete()
        await callback.answer()
    if callback.data == 'nextphoto':
        random_photo = random.choice(list(photos.keys()))
        await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=random_photo,
                             caption=photos[random_photo],
                             reply_markup=ikb)
        await callback.answer()
    if callback.data == 'changephoto':
        # random_photo = random.choice(list(photos.keys()))  # если попадется фотка такая же как и та которую мы изменяем и будет тот же reply_markup, то возникнет исключение, поэтому строчка ниже более правильная.
        # random_photo = random.choice(list(filter(lambda x: x != random_photo, list(photos.keys()))))
        a = random_photo
        while a == random_photo:            # эти три строчки выполняют тоже самое что и строка с лямбдой выше, но этот алгоритм я придумал сам
            random_photo = random.choice(list(photos.keys()))
        await callback.message.edit_media(types.InputMedia(media=random_photo,
                                                           type='photo',
                                                           caption=photos[random_photo],),
                                          reply_markup=ikb)
        await callback.answer()
    if callback.data == 'boom':
        await callback.message.edit_media(types.InputMedia(media='https://www.google.com/imgres?imgurl=http%3A%2F%2Fwww.qli.ru%2Fwp-content%2Fuploads%2Favatarka1.jpeg&tbnid=o9TIG7Dxt9Jt7M&vet=10CHYQMyidAWoXChMIoLGL7uT5_QIVAAAAAB0AAAAAEAM..i&imgrefurl=http%3A%2F%2Fwww.qli.ru%2Ffotki-na-avatarku-o-chem-govoryat%2F&docid=F61vTQbWfOsD3M&w=230&h=238&q=%D1%84%D0%BE%D1%82%D0%BA%D0%B8&ved=0CHYQMyidAWoXChMIoLGL7uT5_QIVAAAAAB0AAAAAEAM',
                                                           type='photo',    # параметр type необязательный
                                                           caption='Woooooooooooow'))
        await callback.answer()
    
        


@dp.inline_handler()
async def inline_command(inline_query: types.InlineQuery):
    text = inline_query.query or 'Empty'
    fat_content = InputTextMessageContent(f'<b>{text}</b>',
                                            parse_mode='html')
    slim_content = InputTextMessageContent(f'<i>{text}</i>',
                                           parse_mode='html')
    contact_content = InputContactMessageContent('89152883024', 'Disney', 'Land')

    item0 = InlineQueryResultArticle(
        input_message_content=contact_content,
        id=str(uuid.uuid4()),
        title='contact',
        description=text,
        thumb_url='https://i.pinimg.com/236x/f5/38/9d/f5389d8bc0855119e7f2015836d50745.jpg'
    )

    item1 = InlineQueryResultArticle(
        input_message_content=fat_content,
        id=str(uuid.uuid4()),
        title='fat',
        description=text,
        thumb_url='https://i.pinimg.com/236x/df/3b/03/df3b03de1413fc7d635f7009a9e0475d.jpg'
    )

    item2 = InlineQueryResultArticle(
        input_message_content=slim_content,
        id=str(uuid.uuid4()),
        title='slim',
        description=text,
        thumb_url='https://i.pinimg.com/236x/c7/f8/52/c7f852640a0845cc87bfbd130f21d438.jpg'
    )
    await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item0, item1, item2],
                                  cache_time=1)






if __name__ == '__main__':
    dp.middleware.setup(TestMiddleware())   # можно зарегистрировать один и тот же класс дважды и тогда весь его функционал будет дублироваться
    dp.middleware.setup(AdminMiddleware())
    dp.middleware.setup(Test2Middleware())
    executor.start_polling(dp, skip_updates=True, on_startup=start)

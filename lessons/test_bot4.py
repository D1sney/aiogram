from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random, asyncio
from aiogram.utils.exceptions import BotBlocked

from aiogram.utils.callback_data import CallbackData        # тема фильтры
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent     # тема Inline режим 
import hashlib
from my_botconfig import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

def ikb_function():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('+', callback_data='btn_+'),
         InlineKeyboardButton('-', callback_data='btn_-')],
         [InlineKeyboardButton('random', callback_data='btn_random')]
    ])
    return ikb


cb = CallbackData('leopard', 'action')      # создается новый шаблон фильтр
like = CallbackData('like', 'action')

ikb = InlineKeyboardMarkup(inline_keyboard=[        # в этом способе создания инлайн клавиатуры, все кнопки созданные в одном списке, будут находиться в одном ряду
    [InlineKeyboardButton('like',callback_data=like.new('like')), InlineKeyboardButton('dislike',callback_data=like.new('dislike'))],[InlineKeyboardButton('close', callback_data=cb.new('push'))]])    # калбэк кнопки close  необходимо отнести к шаблону cb чтобы наш обработчик, представленный ниже, обработал калбэк по фильтру 'cb'
kb1 = InlineKeyboardButton('really?',
                           callback_data='really?')
ikb.add(kb1)

is_voted = False
count = 0


@dp.message_handler(text='one')
async def one_command(message: types.Message):
    await message.answer(f'Ваше число: {count}',
                         reply_markup=ikb_function())

#############################################################################################


@dp.message_handler(text='/start')
async def start_command(message: types.Message):
    await asyncio.sleep(10)
    await bot.send_photo(message.chat.id,
                         photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fbipbap.ru%2Fwp-content%2Fuploads%2F2017%2F04%2F0_7c779_5df17311_orig.jpg&tbnid=6-Qy_SJZBpj82M&vet=12ahUKEwimj7KDkv39AhUDuioKHXKBAWgQMygbegUIARCdAg..i&imgrefurl=https%3A%2F%2Fbipbap.ru%2Fpictures%2Fsamye-krasivye-kartinki-35-foto.html&docid=sEGIYATiGbAkcM&w=1920&h=1200&q=%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B0&ved=2ahUKEwimj7KDkv39AhUDuioKHXKBAWgQMygbegUIARCdAg',
                         caption='Тебе нравится это фото?',
                         reply_markup=ikb)
    

@dp.errors_handler(exception=ZeroDivisionError)
async def error_hand(update: types.Update, exception: all):         # exception внутри функции не фильтрует ошибки, ошибки фильтруются в строчке выше, внутри хэндлера
    print('нельзя отправить сообщение если бота заблокировали')    
    return True


@dp.errors_handler()                                                # хэндлеры ошибок работают немного подругому, если ошибка отловленна выше, она может также быть отловленна другим хэндлером ниже и исполнятся два кода, двух хэндлеров
async def error_hand(update: types.Update, exception: all):
    print('что-то не так')
    await bot.send_message(chat_id=1063427532,                          # если я заблокировал бота, то вызвав исключение исполнится код в котором опять же надо будет отправить сообщение и тогда уже будет исключение которое никак не обрабатывается и бот остановится
                           text=f'{update.message.from_user.full_name} заблокировал бота и не получилось ему отправить сообщение') # если отлавливать ошибку в Inline режиме бота или внутри callback_query_hendler, то там к from_user надо обрашаться не через message, а через inline_query или callback_query соответственно, потому что в таких случаях в update, не будет храниться message
    return True


#############################################################################################

@dp.callback_query_handler(cb.filter())
async def callback_command(callback: types.CallbackQuery, callback_data: dict ):        # фильтрация калбэков происходит через фильтр 'cb'
    if callback_data['action'] == 'push':
        await callback.answer('Фотография закрыта')
        await callback.message.delete()
    # await callback.answer('Фотография закрыта')               # так как в этом фильтре только один калбэк, код который ниже тоже работает и без всякой дополнительной фильтрации
    # await callback.message.delete()



@dp.callback_query_handler(lambda callback_query: callback_query.data=='really?')
async def callback_command(callback: types.CallbackQuery):
    await callback.answer(show_alert = True,
                          text=str(callback.data))



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def btn_command(callback: types.CallbackQuery):
    global count
    if callback.data == 'btn_+':
        count += 1
        await callback.answer(text = f'Ваше число равно: {count}',
                              show_alert=True)
    if callback.data == 'btn_-':
        count -= 1
        await callback.message.edit_text(f'Ваше число: {count}',
                                         reply_markup=ikb_function())  # так как в увеличении числа сообщение не изменяется, если увеличить на один а потом уменьшить, то выйдет исключение что сообщение никак не было измененно
        await callback.answer(text = f'Ваше число равно: {count}') 
    if callback.data == 'btn_random':
        count = random.randint(-10,10)
        await callback.message.edit_text(f'Ваше число равно: {count}',
                                         reply_markup=ikb_function())
        await callback.answer()
    



@dp.callback_query_handler(like.filter(action='like'))
async def callback_command(callback: types.CallbackQuery):
    global is_voted
    if not is_voted:
        is_voted = True
        await callback.answer('Вам понравилась данная фотография!')
    else:
        await callback.answer('Вы уже голосовали',
                              show_alert=True)


@dp.callback_query_handler(like.filter(action='dislike'))
async def callback_command(callback: types.CallbackQuery):
    global is_voted
    if not is_voted:
        is_voted = True
        await callback.answer('Вам не понравилась эта фотка!')
    else:
        await callback.answer('Вы уже голосовали',
                              show_alert=True)



@dp.inline_handler()
async def inline_command(inline_query: types.InlineQuery):
    text = inline_query.query or 'Gang'  # получили текст от пользователя, если сообщение пустое то в переменную text должно сохранятся 'Echo'
    input_content = InputTextMessageContent(f'<b><i>{text}</i></b>',
                                            parse_mode='html')   # формируем контент ответного сообщения
    result_id: str = hashlib.md5(text.encode()).hexdigest()  # сделали уникальный ID результата, путем кодирования текста пользователя сначала в двоичную, а потом в шестнадцатиричную систему исчесления
    # ': str' - это необязательно
    
    # if text == 'photo':
    #     input_content = InputTextMessageContent('This is photo')    # такой вариант гораздо проще и именно его предлагают в курсе, при нем можно не добавлять второй item и второй bot.answer

    item = InlineQueryResultArticle(
        input_message_content=input_content,
        id=result_id,
        title=text
    )

    item2 = InlineQueryResultArticle(
        input_message_content=InputTextMessageContent('This is photo'),
        id=result_id,
        title='Фоточка',
        description='наконец-то ты напечатал что-то...'
    )

    if text == 'photo':
        await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item2],
                                  cache_time=1)  # время через которое будут кэшироваться данные
        await bot.send_message(chat_id=1063427532,
                               text=f'{inline_query.from_user.username} напечатал photo через Inline режим')
    else:
        await bot.answer_inline_query(inline_query_id=inline_query.id,
                                      results=[item],
                                      cache_time=1)  # время через которое будут кэшироваться данные
        


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
from aiogram import Dispatcher, Bot, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State     # для машины состояний
from aiogram.dispatcher import FSMContext       # для машины состояний
from my_botconfig import TOKEN_API

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot,
               storage=storage)

def get_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Начать работу!!!')).add(KeyboardButton('/show')).add(KeyboardButton('/signin'))
    return kb

def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cansel')).add(KeyboardButton('/inlinetest'))

def get_inline():
    return InlineKeyboardMarkup().add(InlineKeyboardButton('no state',callback_data='nostate')).add(InlineKeyboardButton('photo state',callback_data='photostate')).add(InlineKeyboardButton('change state',callback_data='changestate'))

class AnketaStatesGroup(StatesGroup):
    photo = State()
    age = State()
    name = State()
    desc = State()

class ClientStatesGroup(StatesGroup):
    photo = State()
    desc = State()


@dp.callback_query_handler(text='nostate', state=None)
async def callback_cmd(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('No state')

@dp.callback_query_handler(text='photostate', state=AnketaStatesGroup.photo)        # калбэки также дополнительно фильтруются по состояниям как и обычные сообщения
async def callback2_cmd(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Photo state')

@dp.callback_query_handler(text='changestate', state='*')
async def callback3_cmd(callback: types.CallbackQuery, state: FSMContext):
    await AnketaStatesGroup.next()
    await callback.answer(text=f'now {await state.get_state()}')

@dp.message_handler(commands=['inlinetest'], state='*')
async def inline_test_cmd(message: types.Message, state: FSMContext):
    await message.answer('Choose please',
                         reply_markup=get_inline())



@dp.message_handler(Text(equals='start'))
@dp.message_handler(Text(equals='начать'))          # на запуск этой функции сработает любой из хэндлеров, достаточно выполнения одного любого условия
@dp.message_handler(commands=['start'], state='*')     # по умолчанию состояние = None
async def start_command(message: types.Message, state: FSMContext):
    await message.answer('Добро пожаловать!!!',
                         reply_markup=get_keyboard())


@dp.message_handler(commands=['cansel'], state=['*']) #  * - означает все состояния        # если в хэндлере не указанны состояния в которых он принимает сообщения, то будут приниматься сообщения только в состояние None, так-как по умолчанию во всех хэндлерах None
async def cansel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()     # проверка текущего состояния, написать в строчке ниже просто if state is None - неправильно
    if current_state is None:             
        print(await state.get_state())
        return
    
    await message.reply('Отменил',
                        reply_markup=get_keyboard())
    print(await state.get_state())
    await state.finish()
    print(await state.get_state())
    async with state.proxy() as data:
        print(data)


@dp.message_handler(commands=['show'], state='*')     # по умолчанию состояние = None
async def start_command(message: types.Message, state: FSMContext):
    await message.answer('лови')
    await ClientStatesGroup.next()
    print(await state.get_state())
    async with state.proxy() as data:
        print(data)
        await bot.send_photo(chat_id=message.chat.id,
                             photo=data['photo'],
                             caption=data['desc'])


@dp.message_handler(commands=['signin'], state='*')
async def signin_cmd(message: types.Message):
    await AnketaStatesGroup.photo.set()
    await message.answer('Show your face')

@dp.message_handler(lambda message: not message.photo, state=AnketaStatesGroup.photo)
async def check_avatar(message: types.Message):
    return await message.reply('Это не ты!')

@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=AnketaStatesGroup.photo)
async def load_avatar(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['avatar'] = message.photo[0].file_id
        print(data)
    await message.reply('А теперь отправь свой возраст')
    await AnketaStatesGroup.next()

@dp.message_handler(lambda message: not message.text.isdigit() , state=AnketaStatesGroup.age)    # isdigit() - это встроенный метод в aiogram, который проверяет является ли текст сообщения ЦЕЛЫМ положительным числом числом
async def check_age(message: types.Message):
    await message.reply('Это не цифра нифига')

@dp.message_handler(lambda message: not message.text.isdigit() or  float(message.text) > 100.0 or float(message.text) < 0.0, state=AnketaStatesGroup.age)    # isdigit() - это встроенный метод в aiogram, который проверяет является ли текст сообщения ЦЕЛЫМ положительным числом числом
async def check_age(message: types.Message):
    await message.reply('Это не возраст нифига')

@dp.message_handler(lambda message: message.text.isdigit(), state=AnketaStatesGroup.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
        print(data)
    await message.reply('А теперь отправь свое имя')
    await AnketaStatesGroup.next()

@dp.message_handler(lambda message: len(message.text) < 4,state=AnketaStatesGroup.name)     # проверка на количество символов в имени
async def load_name(message: types.Message, state: FSMContext):
    await message.reply('Имя короткое')


@dp.message_handler(state=AnketaStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        print(data)
    await message.reply('А теперь расскажи немного о себе')
    await AnketaStatesGroup.next()

@dp.message_handler(state=AnketaStatesGroup.desc)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
        print(data)
    await message.reply('Все сохраненно')
    await AnketaStatesGroup.next()
    print(await state.get_state())
    async with state.proxy() as data:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=data['avatar'],
                             caption=f"{data['desc']} {data['age']} {data['name']}\n{data['about']}")           # MemoryStorage() сохраняет данные из разных групп состояний
    await ClientStatesGroup.next()          # если во время цикла одной группы состояний вызвать next в другой группе состояний, то независимо от того на каком состояние до этого прервался цикл в этой группе состояний, он начнется с первого состояния как при самом первом вызове (не запоминаются предыдущие состояния в других группах состояний)
    print(await state.get_state())






@dp.message_handler(Text(equals='Начать работу!!!', ignore_case=True), state='*')            # ignore_case при значении True игнорирует состояние регистра, можно писать в перемешку заглавные и маленькие
async def work_command(message: types.Message, state: FSMContext):
    print(await state.get_state())
    await ClientStatesGroup.next()                  # в самом начале можно тоже использовать next() и тогда цикл состояний начнется с первого состояния, также как и строчкой ниже с состояния photo
    # await ClientStatesGroup.photo.set()       
    await message.answer('Сначала отправь фотку!',
                         reply_markup=get_cancel())
    print(await state.get_state())

@dp.message_handler(lambda message: not message.photo, state=ClientStatesGroup.photo)
async def check_photo(message: types.Message):
    return await message.reply('Это не фотография!')

@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=ClientStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):    
    if message.media_group_id:          
        return                              # эта проверка для того чтобы пользователь не отправлял несколько фото в одном сообщении, если он так делает то в message появляется media_group_id, и тогда мы с помощью return прерываем функцию, а если пользователь отправляет только одну фотку, то код функции исполняется дальше                   
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.reply('А теперь отправь описание')
    await ClientStatesGroup.next()                          # при постоянном повторе next() в одной группе состояний после последнего состояния будет состояние None, но данные сохраненные в MemoryStorage() не удалятся как после state.finish(), а потом если еще раз использовать next(), цикл начнется заново с первого состояния



@dp.message_handler(state=ClientStatesGroup.desc)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.reply('отлично')
    await message.reply('Все сохраненно')
    
    async with state.proxy() as data:
        print(data)
        await bot.send_photo(chat_id=message.chat.id,
                             photo=data['photo'],
                             caption=data['desc'])
    print(await state.get_state())
    # await state.finish()            # после этой команды все что вы сохранили в MemoryStorage() удалится (и данные, и состояния)
    print(await state.get_state())




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
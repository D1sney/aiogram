from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import random, os
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def start(_):
    print('Your Story work')





kb=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('Избранное', callback_data='lovelystories'), KeyboardButton('Читать истории', callback_data='allstories')]
    ])

ikb=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('❤️Добавить в избранное', callback_data='like_common'), InlineKeyboardButton('Удалить из избранного💔', callback_data='diz_like')],
    [InlineKeyboardButton('Седующая история🚪', callback_data='next')],
    [InlineKeyboardButton('Закрыть⚰️', callback_data='close')],
    ])

love_ikb=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Удалить🔪🩸', callback_data='diz_love_like')],
    [InlineKeyboardButton('⬅️', callback_data='swipe_<==='), InlineKeyboardButton('➡️', callback_data='swipe_===>') ],
    [InlineKeyboardButton('Закрыть🪦', callback_data='close')],
    ])

love_ikb_1=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Удалить🔪🩸', callback_data='diz_love_like')],
    [InlineKeyboardButton('Закрыть🪦', callback_data='close')],
    ])

dizlove_ikb=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Вернуть🧟‍♂️', callback_data='like_love')],
    [InlineKeyboardButton('⬅️', callback_data='swipe_<='), InlineKeyboardButton('➡️', callback_data='swipe_===>') ],
    [InlineKeyboardButton('Закрыть🪦', callback_data='close')],
    ])

dizlove_ikb_1=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Вернуть🧟‍♂️', callback_data='like_love')],
    [InlineKeyboardButton('Закрыть🪦', callback_data='close')],
    ])

@dp.message_handler(commands=['start', 'description'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=f'''
<b><i>Привет {message.from_user.full_name}, я бот который умеет рассказвать страшилки!</i></b>💬
⚫️Ты можешь добавлять истории в <i>избранное</i> чтобы никогда их не потерять🔝
⚫️В избранном у тебя есть удобная система навигации по твоим любимым истроиям, все чтобы ты быстрее находил твою любимую историю!♥️
⚫️Если ты случайно удалил историю из избранного, не переживай ты можешь мгновенно вернуть её на прежнее место🪦
⚫️Чтобы не засорять диалог, ты можешь нажать на кнопку <b><i>закрыть</i></b> на любом сообщении, когда захочешь🪓
''',
                           reply_markup=kb,
                           parse_mode='html')    
    await bot.send_message(chat_id=1063427532,
                           text=f'''@{message.from_user.username} написал боту 
ID: {message.from_user.id}''')    
    await message.delete()




@dp.message_handler(text='Читать истории')
async def read_command(message: types.Message):
    pictures = []
    teksts = []
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\stories.txt', 'r', encoding='utf8')
    picture = file.readline()
    while picture != '':
        tekst = file.readline()
        picture = picture.rstrip('\n')                  # считывает все истории из базы историй
        tekst = tekst.rstrip('\n')
        pictures.append(picture)
        teksts.append(tekst)
        picture = file.readline()
    file.close()
    photos = dict(zip(pictures, teksts))
    random_photo = random.choice(list(photos.keys()))   
    
    idishnik = await bot.send_photo(chat_id=message.chat.id,                    # idishnik берет информацию о сообщени, нам это нужно чтобы узнать точный ID сообщения для будущего удаления его                  
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)
    await message.delete()
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'r', encoding='utf8')
    flag = False
    id = file.readline()
    while id != '':
        id = int(id)
        skip_photo_id = file.readline()                         # проверяет есть такой пользователь, если нет то записывает в конец файла random_story его текущую историю, если есть, то меняет прошлую текущую историю на настоящую 
        if id == message.chat.id:
            flag = True
        id = file.readline()
    file.close()
    if flag == False:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'a', encoding='utf8')
        file.write(f'{message.chat.id}\n{random_photo}\n')
        file.close()
    else:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'r', encoding='utf8')
        newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_random_story_now.txt', 'w', encoding='utf8')
        id = file.readline()
        while id != '':
            id = int(id)
            skip_photo_id = file.readline()
            if id == message.chat.id:
                newfile.write(f'{id}\n{random_photo}\n')
            else:
                newfile.write(f'{id}\n{skip_photo_id}')
            id = file.readline()    
        file.close()
        newfile.close()
        os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt')
        os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_random_story_now.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt')
    
    # все операции с будущим удалением окна "Читать Истории"
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_story.txt', 'r', encoding='utf8')
    flag = False   
    id = file.readline()
    while id != '':
        id = int(id)
        nowmessage_id = file.readline()                         # проверяет есть ли такой пользователь
        if id == message.chat.id:
            delete_id = float(nowmessage_id)
            flag = True
        id = file.readline()
    file.close()
    if flag == False:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_story.txt', 'a', encoding='utf8')
        file.write(f'{message.chat.id}\n{idishnik.message_id}\n')
        file.close()
    if flag == True:
        try:
            await bot.delete_message(chat_id = message.chat.id, message_id=delete_id)
        except:
            pass
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_story.txt', 'r', encoding='utf8')
    newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\new_id_story.txt', 'w', encoding='utf8')
    id = file.readline()
    while id != '':
        id = int(id)
        nowmessage_id = file.readline()
        if id == message.chat.id:
            newfile.write(f'{id}\n{idishnik.message_id}\n')
        else:
            newfile.write(f'{id}\n{nowmessage_id}')
        id = file.readline()    
    file.close()
    newfile.close()
    os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_story.txt')
    os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\new_id_story.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_story.txt')







@dp.message_handler(text='Избранное')
async def read_love_command(message: types.Message):               
    position = 0
    flag = False
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt', 'r', encoding='utf8')
    id = file.readline()
    while id != '':
        id = int(id)
        skip_position = file.readline()
        if id == message.chat.id:
            flag = True
            position = int(float(skip_position))
        id = file.readline()
    file.close()
    if flag == False:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt', 'a', encoding='utf8')
        file.write(f'{message.chat.id}\n0\n')
        file.close()
    try:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
    except FileNotFoundError:
        await message.answer('У вас пока нету фотографий в избранном')
    else:
        count = 0
        flag2 = False
        love_pictures = []
        love_teksts = []
        love_picture = file.readline()
        while love_picture != '':
            count += 1
            flag2 = True
            love_tekst = file.readline()
            love_picture = love_picture.rstrip('\n')       # rstrip('\n') для love_pictures, love_teksts
            love_tekst = love_tekst.rstrip('\n')
            love_pictures.append(love_picture)
            love_teksts.append(love_tekst)
            love_picture = file.readline()
        file.close()
        if flag2 == True:                                        # флаг показывает есть ли в данный момент истории в избранном или нет
            if count == 1:    
                idishnik = await bot.send_photo(chat_id=message.chat.id,
                                photo=love_pictures[position],
                                caption=love_teksts[position],
                                reply_markup=love_ikb_1)
            else:
                idishnik = await bot.send_photo(chat_id=message.chat.id,                    # idishnik берет информацию о сообщени, нам это нужно чтобы узнать точный ID сообщения для будущего удаления его
                                photo=love_pictures[position],
                                caption=love_teksts[position],
                                reply_markup=love_ikb)
            flag3 = False
            file = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\love_story_now.txt', 'r', encoding='utf8')
            id = file.readline()
            while id != '':
                id = int(id)
                skip_love_photo = file.readline()
                if id == message.chat.id:
                    flag3 = True
                id = file.readline()
            file.close()
            if flag3 == False:
                file = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\love_story_now.txt', 'a', encoding='utf8')
                file.write(f'{message.chat.id}\n{love_pictures[position]}\n')
                file.close()
            else:
                file = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\love_story_now.txt', 'r', encoding='utf8')
                newfile = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\new_love_story_now.txt', 'w', encoding='utf8')
                id = file.readline()
                while id != '':
                    id = int(id)
                    skip_love_photo = file.readline()
                    if id == message.chat.id:
                        newfile.write(f'{id}\n{love_pictures[position]}\n')                  # обновляет данные в love_story_now при вызове "любимые истории"
                    else:
                        newfile.write(f'{id}\n{skip_love_photo}')
                    id = file.readline()    
                file.close()
                newfile.close()
                os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\love_story_now.txt')
                os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_love_story_now.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\love_story_now.txt')
        else:
            await message.answer('У вас сейчас нету фотографий в избранном')

        # все операции с будущим удалением окна "Читать Истории"
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_love_story.txt', 'r', encoding='utf8')
        flag = False   
        id = file.readline()
        while id != '':
            id = int(id)
            nowmessage_id = file.readline()                         # проверяет есть ли такой пользователь
            if id == message.chat.id:
                delete_id = float(nowmessage_id)
                flag = True
            id = file.readline()
        file.close()
        if flag == False:
            file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_love_story.txt', 'a', encoding='utf8')
            file.write(f'{message.chat.id}\n{idishnik.message_id}\n')
            file.close()
        if flag == True:
            try:
                await bot.delete_message(chat_id = message.chat.id, message_id=delete_id)
            except:
                pass
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_love_story.txt', 'r', encoding='utf8')
        newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\new_id_love_story.txt', 'w', encoding='utf8')
        id = file.readline()
        while id != '':
            id = int(id)
            nowmessage_id = file.readline()
            if id == message.chat.id:
                newfile.write(f'{id}\n{idishnik.message_id}\n')
            else:
                newfile.write(f'{id}\n{nowmessage_id}')
            id = file.readline()    
        file.close()
        newfile.close()
        os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_love_story.txt')
        os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\new_id_love_story.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\id_love_story.txt')
    finally:
        await message.delete()                      





@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('swipe'))
async def swipe_command(callback: types.CallbackQuery):
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
    count = 0
    love_pictures = []
    love_teksts = []
    love_picture = file.readline()
    while love_picture != '':
        count +=1 
        love_tekst = file.readline()
        love_picture = love_picture.rstrip('\n')                # считывает любимые истории пользователя 
        love_tekst = love_tekst.rstrip('\n')
        love_pictures.append(love_picture)
        love_teksts.append(love_tekst)
        love_picture = file.readline()
    file.close()

    position = 0
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt', 'r', encoding='utf8')
    newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_tochka_chtenia.txt', 'w', encoding='utf8')
    id = file.readline()
    while id != '':
        skip_position = file.readline()
        id = int(id)
        skip_position = float(skip_position)
        if id == callback.message.chat.id:
            position = int(skip_position)
            if callback.data == 'swipe_<=':
                pass                                #position = position тоже работает
            if callback.data == 'swipe_<===':
                if position == 0:
                    position = (len(love_pictures) - 1)                     # изменяет точку чтения, чтобы далее вывести предыдущую историю
                else:
                    position -= 1
            if callback.data == 'swipe_===>':
                if position == len(love_pictures) - 1:
                    position = 0
                else:
                    position += 1
            newfile.write(f'{id}\n{position}\n')
        else:
            newfile.write(f'{id}\n{skip_position}\n')
        id = file.readline()   
    file.close()
    newfile.close()
    os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt')
    os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_tochka_chtenia.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt')
    
    if count == 1:
        await callback.message.edit_media(types.InputMedia(media=love_pictures[position], type='photo', caption=love_teksts[position]), reply_markup=love_ikb_1)
    else:
        await callback.message.edit_media(types.InputMedia(media=love_pictures[position], type='photo', caption=love_teksts[position]), reply_markup=love_ikb)

    file = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\love_story_now.txt', 'r', encoding='utf8')
    newfile = open(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\new_love_story_now.txt', 'w', encoding='utf8')
    id = file.readline()
    while id != '':
        id = int(id)
        skip_love_photo = file.readline()
        if id == callback.message.chat.id:
            newfile.write(f'{id}\n{love_pictures[position]}\n')                  # обновляет данные в love_story_now при вызове "любимые истории"
        else:
            newfile.write(f'{id}\n{skip_love_photo}')
        id = file.readline()    
    file.close()
    newfile.close()
    os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\love_story_now.txt')
    os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_love_story_now.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\love_story_now.txt')








@dp.callback_query_handler(text='next')
async def next_command(callback: types.CallbackQuery):
    pictures = []
    teksts = []
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\stories.txt', 'r', encoding='utf8')
    picture = file.readline()
    while picture != '':
        tekst = file.readline()
        picture = picture.rstrip('\n')                  # считывает все истории из базы историй
        tekst = tekst.rstrip('\n')
        pictures.append(picture)
        teksts.append(tekst)
        picture = file.readline()
    file.close()
    photos = dict(zip(pictures, teksts))
    random_photo = random.choice(list(photos.keys())) 

    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'r', encoding='utf8')
    id = file.readline()
    while id != '':
        skip_photo_id = file.readline()
        id = int(id)
        if id == callback.message.chat.id:
            photo_id = skip_photo_id.rstrip('\n')
        id = file.readline()
    file.close()
    while random_photo == photo_id:
        random_photo = random.choice(list(photos.keys()))    
    await callback.message.edit_media(types.InputMedia(media=random_photo, type='photo', caption=photos[random_photo]), reply_markup=ikb)

    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'r', encoding='utf8')
    newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_random_story_now.txt', 'w', encoding='utf8')

    id = file.readline()
    while id != '':
        id = int(id)
        skip_photo_id = file.readline()
        if id == callback.message.chat.id:
            newfile.write(f'{id}\n{random_photo}\n')
        else:
            newfile.write(f'{id}\n{skip_photo_id}')
        id = file.readline()    
    file.close()
    newfile.close()
    os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt')
    os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_random_story_now.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt')

                                                                                                                        






@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('like'))
async def like_command(callback: types.CallbackQuery):
    pictures = []
    teksts = []
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\stories.txt', 'r', encoding='utf8')
    picture = file.readline()
    while picture != '':
        tekst = file.readline()
        picture = picture.rstrip('\n')                  # считывает все истории из базы историй
        tekst = tekst.rstrip('\n')
        pictures.append(picture)
        teksts.append(tekst)
        picture = file.readline()
    file.close()
    photos = dict(zip(pictures, teksts))
    
    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'r', encoding='utf8')
    id = file.readline()
    while id != '':
        skip_photo = file.readline()
        id = int(id)                                        # узнает текущую фотографию в разделе "Читать истории"
        if id == callback.message.chat.id:
            now_photo = skip_photo.rstrip('\n')
        id = file.readline()
    file.close()

    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\love_story_now.txt', 'r', encoding='utf8')
    id = file.readline()
    while id != '':
        skip_photo = file.readline()
        id = int(id)                                        # узнает текущую фотографию в любимых историях
        if id == callback.message.chat.id:
            now_love_photo = skip_photo.rstrip('\n')
        id = file.readline()
    file.close()

    if callback.data == 'like_love':
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
        love_pictures = []
        love_teksts = []
        love_picture = file.readline()
        while love_picture != '':
            love_tekst = file.readline()
            love_picture = love_picture.rstrip('\n')                # считывает любимые истории пользователя для len(love_pictures)
            love_tekst = love_tekst.rstrip('\n')
            love_pictures.append(love_picture)
            love_teksts.append(love_tekst)
            love_picture = file.readline()
        file.close()
        if len(love_pictures) == 0:
            await callback.message.edit_media(types.InputMedia(media=now_love_photo, type='photo', caption=photos[now_love_photo]), reply_markup=love_ikb_1)
        else:
            await callback.message.edit_media(types.InputMedia(media=now_love_photo, type='photo', caption=photos[now_love_photo]), reply_markup=love_ikb)

    try:     
        if callback.data == 'like_common':
            now_picture = now_photo
        elif callback.data == 'like_love':
            now_picture = now_love_photo      
        flag = False
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
        name = file.readline()
        while name != '':
            name = name.rstrip('\n')
            if name == now_picture:
                await callback.answer('Эта история уже добавленна в избранное')
                flag = True
            skip_text = file.readline()                                                     # добавляет текущую историю в любимые если она еще не добавлена, если добавлена то выводит соответствующее сообщение
            name = file.readline()
        file.close()
        if flag == False:
            if callback.data == 'like_common':
                file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'a', encoding='utf8')
                file.write(f'{now_photo}\n{photos[now_photo]}\n')
                file.close()
                await callback.answer('История добавлена в избранное')
            if callback.data == 'like_love':
                file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
                love_pictures = []
                love_teksts = []
                love_picture = file.readline()
                while love_picture != '':
                    love_tekst = file.readline()
                    love_picture = love_picture.rstrip('\n')                # считывает любимые истории пользователя для len(love_pictures)
                    love_tekst = love_tekst.rstrip('\n')
                    love_pictures.append(love_picture)
                    love_teksts.append(love_tekst)
                    love_picture = file.readline()
                file.close() 

                file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt', 'r', encoding='utf8')
                newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_tochka_chtenia.txt', 'w', encoding='utf8')
                id = file.readline()
                while id != '':
                    skip_position = file.readline()
                    id = int(id)
                    skip_position = float(skip_position)
                    if id == callback.message.chat.id:
                        position = int(skip_position)                                             
                        if len(love_pictures) == 0:
                            position = 0
                        else:                                               
                            if position != len(love_pictures) - 1:                              # возвращение предыдущей точки доступа
                                position += 1
                            else:
                                if position != skip_position:
                                    position = 0
                                else:
                                    position += 1
                        newfile.write(f'{id}\n{position}\n')
                    else:
                        newfile.write(f'{id}\n{skip_position}\n')
                    id = file.readline()   
                file.close()
                newfile.close()
                os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt')
                os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_tochka_chtenia.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt')

                file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
                newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\new' + str(callback.message.chat.id) + '.txt', 'w', encoding='utf8')
                flag = False
                count = 0
                like_photo = file.readline()
                while like_photo != '':
                    like_caption = file.readline()
                    if count == position:
                        flag = True
                        newfile.write(f'{now_love_photo}\n{photos[now_love_photo]}\n')              # записывает историю на ее место до удаления из избранного
                    newfile.write(f'{like_photo}{like_caption}')
                    like_photo = file.readline()
                    count += 1
                if flag == False:
                    newfile.write(f'{now_love_photo}\n{photos[now_love_photo]}\n')
                file.close()
                newfile.close()                
                os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt')
                os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\new' + str(callback.message.chat.id) + '.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt')

                await callback.answer('История возвращенна в избранное на прежнее место')

    except FileNotFoundError:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'a', encoding='utf8')
        file.write(f'{now_photo}\n{photos[now_photo]}\n')
        file.close()
        await callback.answer('История добавлена в избранное')









@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('diz'))
async def dizlike_command(callback: types.CallbackQuery):
    if callback.data == 'diz_like':
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\random_story_now.txt', 'r', encoding='utf8')
    elif callback.data == 'diz_love_like':
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\love_story_now.txt', 'r', encoding='utf8')
    id = file.readline()
    while id != '':
        skip_photo = file.readline()
        id = int(id)                                        # узнает текущую фотографию в разделе "Читать истории"
        if id == callback.message.chat.id:
            now_photo = skip_photo.rstrip('\n')
        id = file.readline()
    file.close()

    if callback.data == 'diz_love_like':       
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt', 'r', encoding='utf8')
        id = file.readline()
        while id != '':
            id = int(id)
            skip_position = file.readline()
            if id == callback.message.chat.id:              # узнает позицию для изменения клавиатуры после калбэка дизлайк
                position = int(float(skip_position))
            id = file.readline()
        file.close()
        
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
        love_pictures = []
        love_teksts = []
        love_picture = file.readline()
        while love_picture != '':
            love_tekst = file.readline()
            love_picture = love_picture.rstrip('\n')                # считывает любимые истории пользователя для len(love_pictures)
            love_tekst = love_tekst.rstrip('\n')
            love_pictures.append(love_picture)
            love_teksts.append(love_tekst)
            love_picture = file.readline()
        file.close()
        if len(love_pictures) == 1:
            await callback.message.edit_media(types.InputMedia(media=now_photo, type='photo', caption=love_teksts[position]), reply_markup=dizlove_ikb_1)       # изменяет клавиатуру в сообщении где есть кнопка вернуть
        else:           
            await callback.message.edit_media(types.InputMedia(media=now_photo, type='photo', caption=love_teksts[position]), reply_markup=dizlove_ikb)

    file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
    flag = False
    like_photo = file.readline()
    while like_photo != '':
        like_caption = file.readline()
        like_photo = like_photo.rstrip('\n')                # проверка есть ли текущая фотография в избранном
        if like_photo == now_photo:
            flag = True
        like_photo = file.readline()
    file.close()

    if flag == False:
        await callback.answer('У вас нет этой истории в избранном')
    else:
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
        newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\new' + str(callback.message.chat.id) + '.txt', 'w', encoding='utf8')
        like_photo = file.readline()
        while like_photo != '':
            like_caption = file.readline()
            like_photo = like_photo.rstrip('\n')                
            if like_photo != now_photo:    
                newfile.write(f'{like_photo}\n{like_caption}')              # если данная история есть в избранном то происходит её удаление, если её нет, то выводится соответствующее сообщение
            like_photo = file.readline()
        file.close()
        newfile.close()
        os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt')
        os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\new' + str(callback.message.chat.id) + '.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt')
        await callback.answer('Данная история была удалена из избранного')

        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\accounts\\' + str(callback.message.chat.id) + '.txt', 'r', encoding='utf8')
        love_pictures = []
        love_teksts = []
        love_picture = file.readline()
        while love_picture != '':
            love_tekst = file.readline()
            love_picture = love_picture.rstrip('\n')                # считывает любимые истории пользователя для len(love_pictures)
            love_tekst = love_tekst.rstrip('\n')
            love_pictures.append(love_picture)
            love_teksts.append(love_tekst)
            love_picture = file.readline()
        file.close() 
        
        file = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt', 'r', encoding='utf8')
        newfile = open( r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_tochka_chtenia.txt', 'w', encoding='utf8')
        id = file.readline()
        while id != '':
            skip_position = file.readline()
            id = int(id)
            skip_position = float(skip_position)
            if id == callback.message.chat.id:
                position = int(skip_position)
                if callback.data == 'diz_like':
                    if len(love_pictures) != 0:
                        position = len(love_pictures) - 1                               # изменение позиции чтения при дизлайке
                    else:
                        position = 0
                if callback.data == 'diz_love_like':
                    if position != 0:
                        position -=1
                    else:
                        if len(love_pictures) != 0:
                            position = len(love_pictures) - 1
                            # для определения предыдущей позиции
                            position += 0.036 
                        else:
                            position = 0
                newfile.write(f'{id}\n{position}\n')
            else:
                newfile.write(f'{id}\n{skip_position}\n')
            id = file.readline()   
        file.close()
        newfile.close()
        os.remove(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt')
        os.rename(r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\new_tochka_chtenia.txt', r'C:\Users\ivan3\OneDrive\Рабочий стол\YourStory\YourStory_PC_version\\tochka_chtenia.txt')


@dp.callback_query_handler(text='close')
async def close_command(callback: types.CallbackQuery):
    await callback.answer('Окно удаленно')
    #await callback.message.delete()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)








if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start)


import asyncio
import time



async def one_second():
    seconds = 0
    while True:    
        await asyncio.sleep(1)
        seconds +=1
        if seconds%3 != 0:
            print(f'прошло {seconds} секунд')

async def three_seconds():
    n = 0
    while True:
        await asyncio.sleep(3)        
        n+=3
        print(f'прошло еще {n} секунды')

async def show_seconds():
    task1 = asyncio.create_task(one_second())
    task2 = asyncio.create_task(three_seconds())

    await task1
    await task2


async def send_hello():
    await asyncio.sleep(3)
    print('hello')

async def send_bye():
    await asyncio.sleep(1)
    print('bye')

async def main():
    await asyncio.create_task(send_hello())      # создает не конкурентные задачи
    await asyncio.create_task(send_bye())

    task1 = asyncio.create_task(send_hello())    # создает конкурентные задачи
    task2 = asyncio.create_task(send_bye())
    await task1
    await task2

async def glavnoe():
    task1 = asyncio.create_task(show_seconds())
    task2 = asyncio.create_task(main())
    await task1
    await task2

asyncio.run(main())

#-----------------------------------------------------------------------------------#

async def secs(sec):
    while True:
        await asyncio.sleep(sec)
        print(f'прошло {sec} секунд')


async def secs_main():
    task1 = asyncio.create_task(secs(2))         # каждый новый вызов асинхронной функции (корутины) создает новый уникальный объект корутины
    task2 = asyncio.create_task(secs(5))         
    await task1                     # в этом случае задачи выполняются конкурентно
    await task2

    # await asyncio.create_task(secs(2))        # в таком случае задачи выполняются последовательно, а не конкурентно
    # await asyncio.create_task(secs(5))

asyncio.run(secs_main())


import aiogram

import config
import logging
import datetime
import calendar

from aiogram import Bot, Dispatcher, executor, types
from sqliter import SQLighter
import asyncio

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инит базы
db = SQLighter('Lessons.db')

lessons_time = {
    '1': '8:00-8:40',
    '2': '8:45-9:25',
    '3': '9:30-10:10',
    '4': '10:15:10:55',
    '5': '11:05-11:45',
    '6': '11:55-12:35',
    '7': '12:45-13:25',
    '8': '13:35-14:15',
    '9': '14:20-15:00',
    '10': '15:05-15:45',
    '11': '15:50-16:30',
    '12': '16:35-17:15'
}

where_napomin = {
    '07:45': '1',
    '08:40': '2',
    '09:25': '3',
    '10:10': '4',
    '11:00': '5',
    '11:50': '6',
    '12:40': '7',
    '13:30': '8',
    '14:15': '9',
    '15:00 ': '10',
    '15:45 ': '11',
    '16:30 ': '12'
}

days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']


def talk_date():
    ser = {'Mon': 'понедельник', "Tue": 'вторник', 'Wed': 'среда', 'Thu': 'четверг', 'Fri': 'пятница', 'Sat': 'суббота',
           'Sun': 'воскресенье'}
    day = str(calendar.day_abbr[datetime.datetime.now().weekday()])
    return ser[day]


def napominalka():
    day1 = talk_date()
    time = str(datetime.datetime.now()).split()[1]
    itog_time = ':'.join(time.split(':')[:2])
    spis = list()
    try:
        subscr = db.get_subscriptions()
        for i in subscr:
            lesson = where_napomin[itog_time]
            inform = db.check_lesson(i[1], day1, lesson)
            if inform[0][4] != 'ничего':
                spis.append(f'{i[1]} {inform[0][4]}')
    except:
        spis.append(f'стоп')
    return spis


napominalka()


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exist(message.from_user.id):
        # если юзера нет
        db.add_subscriber(message.from_user.id, True)
    else:
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы успешно подписались на рассылку ждите новостей )))")


@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exist(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы итак не подписаны')
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки (((")


@dp.message_handler(commands=['lessons_time'])
async def subscribe(message: types.Message):
    st = ''
    for i in lessons_time.keys():
        st1 = f'{i}) {lessons_time[i]}' + "\n"
        st += st1
    await  bot.send_message(message.from_user.id, st)


@dp.message_handler(commands=['my_lessons'])
async def subscribe(message: types.Message):
    for i in days:
        z = f'{i}:' + '\n'
        for j in db.user_search(message.from_user.id, i):
            q = f'{j[3]}. {j[4]}' + '\n'
            z += q
        await bot.send_message(message.from_user.id, z)


@dp.message_handler()
async def subscribe(message: types.Message):
    mes = str(message["text"]).lower().split()
    if len(mes) > 1 and mes[0] in days and mes[1].isdigit() and mes[2] == '-':
        if mes[1] in lessons_time.keys():
            time = lessons_time[mes[1]]
            db.add_lesson(message.from_user.id, mes[0], mes[1], ' '.join(mes[3:]), time)
            await bot.send_message(message.from_user.id, "Всё добавленно")
        else:
            await  bot.send_message(message.from_user.id, "Вы ошиблись")
    elif len(mes) == 1 and mes[0] in days:
        z = f'{mes[0]}:' + '\n'
        for j in db.user_search(message.from_user.id, mes[0]):
            q = f'{j[3]} {j[4]}' + '\n'
            z += q
        await bot.send_message(message.from_user.id, z)
    elif len(mes) == 1 and mes[0] == 'сегодня':
        mes[0] = talk_date()
        z = f'{mes[0]}:' + '\n'
        for j in db.user_search(message.from_user.id, mes[0]):
            q = f'{j[3]} {j[4]}' + '\n'
            z += q
        await bot.send_message(message.from_user.id, z)
    else:
        await  bot.send_message(message.from_user.id, "Вы ошиблись")


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        mes = napominalka()
        for i in mes:
            if i != 'стоп':
                i = i.split()
                await bot.send_message(i[0], f'Ваш следующий урок: {i[1]}')


if __name__ == '__main__':
    dp.loop.create_task(scheduled(60))
    executor.start_polling(dp, skip_updates=True)

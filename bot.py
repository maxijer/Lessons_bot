import aiogram

import config
import logging
import datetime
import calendar

from aiogram import Bot, Dispatcher, executor, types
from sqliter import SQLighter
from OLIMPIADA import Olymp

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
    '10': '15:05-15:45'
}

days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

print(calendar.day_abbr[datetime.datetime.now().weekday()])


def talk_date():
    ser = {'Mon': 'понедельник', "Tue": 'вторник', 'Wed': 'среда', 'Thu': 'четверг', 'Fri': 'пятница', 'Sat': 'суббота', 'Sun': 'воскресенье'}
    day = str(calendar.day_abbr[datetime.datetime.now().weekday()])
    return ser[day]


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
            q = f'{j[3]} {j[4]}' + '\n'
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
    elif len(mes)  == 1 and mes[0] == 'сегодня':
        mes[0] = talk_date()
        z = f'{mes[0]}:' + '\n'
        for j in db.user_search(message.from_user.id, mes[0]):
            q = f'{j[3]} {j[4]}' + '\n'
            z += q
        await bot.send_message(message.from_user.id, z)
    else:
        await  bot.send_message(message.from_user.id, "Вы ошиблись")


@dp.message_handler(commands=['physics'])
async def subscribe(message: types.Message):
    z = db_2.physics()
    for i in z:
        q = str(i[3]).replace('activity', '/files/m_activity')
        print(i)
        try:
            await bot.send_photo(message.from_user.id,
                                 q + '/' + i[4],
                                 caption=i[1] + "\n" + "Общая информация: " + i[
                                     2] + "\n" + "Более подробная информация по ссылке: " + "\n" + i[3],
                                 disable_notification=True)
        except Exception as e:
            if str(e) == "Media_caption_too_long":
                new = '1'
                await bot.send_photo(message.from_user.id,
                                     q + '/' + i[4],
                                     caption=i[1] + "\n" + "Общая информация: " + new[
                                         0] + "\n",
                                     disable_notification=True)
                for t in new[1:]:
                    await bot.send_message(message.from_user.id, t)
                await  bot.send_message(message.from_user.id, "Более подробная информация по ссылке: " + "\n" + i[3])
            else:
                new = my_spliter(i[2])
                print(q)
                for t in new:
                    await bot.send_message(message.from_user.id, t)
                await  bot.send_message(message.from_user.id, "Более подробная информация по ссылке: " + "\n" + i[3])


@dp.message_handler(commands=['math'])
async def subscribe(message: types.Message):
    z = db_2.math()
    z = z
    for i in z:
        q = str(i[3]).replace('activity', '/files/m_activity')
        try:
            await bot.send_photo(message.from_user.id,
                                 q + '/' + i[4],
                                 caption=i[1] + "\n" + "Общая информация: " + i[
                                     2] + "\n" + "Более подробная информация по ссылке: " + "\n" + i[3],
                                 disable_notification=True)
        except Exception as e:
            if str(e) == "Media_caption_too_long":
                new = my_spliter(i[2])
                await bot.send_photo(message.from_user.id,
                                     q + '/' + i[4],
                                     caption=i[1] + "\n" + "Общая информация: " + new[
                                         0] + "\n",
                                     disable_notification=True)
                for t in new[1:]:
                    await bot.send_message(message.from_user.id, t)
                await  bot.send_message(message.from_user.id, "Более подробная информация по ссылке: " + "\n" + i[3])
            else:
                new = my_spliter(i[2])
                print(q)
                for t in new:
                    await bot.send_message(message.from_user.id, t)
                await  bot.send_message(message.from_user.id, "Более подробная информация по ссылке: " + "\n" + i[3])


@dp.message_handler(commands=['inform'])
async def subscribe(message: types.Message):
    z = db_2.inform()
    for i in z:
        q = str(i[3]).replace('activity', '/files/m_activity')
        try:
            await bot.send_photo(message.from_user.id,
                                 q + '/' + i[4],
                                 caption=i[1] + "\n" + "Общая информация: " + i[
                                     2] + "\n" + "Более подробная информация по ссылке: " + "\n" + i[3],
                                 disable_notification=True)
        except Exception as e:
            if str(e) == "Media_caption_too_long":
                new = my_spliter(i[2])
                await bot.send_photo(message.from_user.id,
                                     q + '/' + i[4],
                                     caption=i[1] + "\n" + "Общая информация: " + new[
                                         0] + "\n",
                                     disable_notification=True)
                for t in new[1:]:
                    await bot.send_message(message.from_user.id, t)
                await  bot.send_message(message.from_user.id, "Более подробная информация по ссылке: " + "\n" + i[3])
            else:
                print(e)


@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exist(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы итак не подписаны')
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки (((")


# async def scheduled(wait_for):
#    while True:
#        await asyncio.sleep(wait_for)
#        now = datetime.utcnow()
#        await bot.send_message(896895871, f'{now}')


if __name__ == '__main__':
    # dp.loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)

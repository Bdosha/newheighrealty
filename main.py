

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

import asyncio
import re

import database
import structure

print('Hello, world')
asyncio.run(asyncio.sleep(10))

#import avito
import ula
import cian
import mirkvartir

# импорт всех библиотек для работы

chat_id: int = -898776545
admins: list = [5663715194, 1132908805]
bot: Bot = Bot('6098152249:AAHvObNBSEzcuEDnzIeZp_wZJKCg4XvwMF4')
dp: Dispatcher = Dispatcher()
root = ['Циан', 'Юла', 'Мир Квартир', "Авито",'Яндекс.Недвижимость']

parce_loop = False
all_objects = []
nums = [str(i) for i in range(100)]


async def msg_new_obj(data, source):
    if source == 1:
        text = f"📍Опубликован новый объект\n" \
               f"📍 Источник: {root[source]}\n" \
               f"<a href = '{data['url']}'>{data['name']}</a>\n" \
               f"💵 {data['price']}\n" \
               f"{data['id']}"
        return text

    text = f"📍Опубликован новый объект\n" \
           f"📍 Источник: {root[source]}\n" \
           f"<a href = '{data['url']}'>{data['name']}</a>\n" \
           f"💵 {data['price']}\n" \
           f"🧭 {data['address']}\n" \
           f"📝 {data['description'][:200]}...\n" \
           f"📆 {data['time']}\n" \
           f"{data['id']}"
    return text


async def parse():
    try:
        print('cringe')
        temps = [
            await cian.houses_source(),
            await cian.flats_source(),
            await ula.houses_source(),
            await ula.flats_source(),
            #await avito.houses_source(),
            #await avito.flats_source(),
            await mirkvartir.houses_source(),
            await mirkvartir.flats_source()
        ]

        all_data = [
            await cian.parse(temps[0]),
            await cian.parse(temps[1]),
            await ula.parse(temps[2]),
            await ula.parse(temps[3]),
            #await avito.parse(temps[4]),
            #await avito.parse(temps[5]),
            await mirkvartir.parse(temps[4]),
            await mirkvartir.parse(temps[5])
        ]

        notification = database.notif_users()
        print(notification)
        for i in range(6):
            data = all_data[i]
            if database.new_object(data['id'], root[i // 2], data['address'], data['name'], data['url']):
                msg_text = str(await msg_new_obj(data, i // 2))
                for user in notification[i // 2]:
                    try:
                        await bot.send_message(chat_id=user,
                                               text=msg_text,
                                               reply_markup=structure.take_work_button,
                                               parse_mode='HTML')
                    except:
                        continue
        await asyncio.sleep(300)
        await parse()
    except TypeError:
        await parse()
    except:

        await parse()


@dp.message(Command(commands=['start']))
async def process_start_command(msg: Message):
    print(msg.from_user.id)
    print(msg.from_user.username, msg.text)
    status = database.check_user(msg.from_user.id)

    if status == -1:
        await msg.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return
    if status == 0:
        await msg.answer(text='Для того, чтобы начать использование бота,'
                              ' требуется пройти регистрацию в системе,'
                              ' пожалуйства ввделите следующие данные в нужном формате:')
        await msg.answer(text='Иванов Иван\n'
                              '+79161234567')
        return
    await msg.answer(text='Вы уже прошли регистрацию и имеете доступ к функция бота',
                     reply_markup=structure.mainkeys[status])


@dp.message(Command(commands=['parse']))
async def process_parse_command(message: Message):
    global parce_loop
    if not parce_loop:
        parce_loop = True
        await parse()
    print('no')


@dp.message(Text(text=['⚙️ Настройки']))
async def settings(message: Message):
    print(message.from_user.username, message.text)

    status = database.check_user(message.from_user.id)
    if status < 1:
        await message.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return

    await message.answer(text='Параметры бота:',
                         reply_markup=structure.make_settings(database.get('users', 'notif', message.from_user.id)))


@dp.message(Text(text=['🤳 Получить номер для прозвона']))
async def get_phone(message: Message):
    print(message.from_user.username, message.text)

    status = database.check_user(message.from_user.id)
    if status < 1:
        await message.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return
    temp = database.get_number()
    if temp == -1:
        await message.answer(text="Нет доступных номеров для обзвона")
        return
    temp = str(temp)
    print(temp)
    if temp[0] == '7':
        temp = '+' + temp
    await message.answer(text=f"Требуется позвонить по номеру:\n{temp}")


@dp.message(Text(text=['🧭 Взяться за объект по ссылке']))
async def help(message: Message):
    print(message.from_user.username, message.text)

    status = database.check_user(message.from_user.id)
    if status < 1:
        await message.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return
    database.set_func(message.from_user.id, 1)

    await message.answer(text='Вставьте ссылку на объект')


@dp.message(Text(text=['🏢 Мои объекты']))
async def profile(message: Message):
    print(message.from_user.username, message.text)
    global all_objects
    all_objects = database.all_work_ob()

    status = database.check_user(message.from_user.id)
    if status < 1:
        await message.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return
    temp = database.get_user_ob(message.from_user.id)
    if not temp:
        await message.answer(text='У вас нет объектов в работе')
        return
    temp = temp[0]
    await message.answer(
        text=f"🔍 Название: {temp[3]}\n"
             f"🧭 Адрес: {temp[2]}\n\n"
             f"📝 Источник: {temp[1]}\n"
             f"▶️ <a href = '{temp[4]}'>Ссылка на объект</a>\n"
             f'<span class="tg-spoiler">{temp[0]}</span>',
        parse_mode='HTML',
        reply_markup=structure.set_page_but('0'))


@dp.message(Text(text=['➕ Добавить номер для прозвона']))
async def new_phone(message: Message):
    print(message.from_user.username, message.text)
    status = database.check_user(message.from_user.id)
    if status < 2:
        await message.answer(text='У вас нет доступа к этой функции', reply_markup=ReplyKeyboardRemove())
        return
    await message.answer(text='Отправьте номера для добавления в базу')
    database.set_func(message.from_user.id, 2)


@dp.callback_query(Text(text=['cancel']))
async def cansel(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)

    await callback.message.edit_text(text='❌ Отменено',
                                     reply_markup=structure.mainkeys[database.check_user(callback.from_user.id)])
    database.set_func(callback.from_user.id, 0)


@dp.callback_query(Text(text=nums))
async def next_object(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)
    temp, now = database.pages(callback.from_user.id, callback.data)
    if not temp:
        await callback.message.edit_text(
            text=f"Нет доступных объектов")
        return
    await callback.message.edit_text(
        text=f"🔍 Название: {temp[3]}\n"
             f"🧭 Адрес: {temp[2]}\n\n"
             f"📝 Источник: {temp[1]}\n"
             f"▶️ <a href = '{temp[4]}'>Ссылка на объект</a>\n"
             f'<span class="tg-spoiler">{temp[0]}</span>',
        parse_mode='HTML',
        reply_markup=structure.set_page_but(now))


@dp.callback_query(Text(text=['-' + i for i in nums]))
async def prev_object(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)
    temp, now = database.pages(callback.from_user.id, callback.data)
    if not temp:
        await callback.message.edit_text(
            text=f"Нет доступных объектов")
        return
    await callback.message.edit_text(
        text=f"🔍 Название: {temp[3]}\n"
             f"🧭 Адрес: {temp[2]}\n\n"
             f"📝 Источник: {temp[1]}\n"
             f"▶️ <a href = '{temp[4]}'>Ссылка на объект</a>\n"
             f'<span class="tg-spoiler">{temp[0]}</span>',
        parse_mode='HTML',
        reply_markup=structure.set_page_but(now))


@dp.callback_query(Text(text=['edit_obj']))
async def cansel(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)
    await callback.message.edit_reply_markup(reply_markup=structure.obj_keys)


@dp.callback_query(Text(text=['delete_obj']))
async def cansel(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)
    await callback.message.edit_text(text='❌ Вы отказались от объекта')
    print(callback.message.text.split("\n")[-1])
    temp = database.delete_obj(callback.from_user.id, callback.message.text.split("\n")[-1])
    if not temp:
        return
    temp = temp[0]

    await bot.send_message(chat_id=chat_id,
                           text=
                           f'📍 Агент прекратил работу с объектом\n\n'
                           f"🔍 Название: {temp[3]}\n"
                           f"🧭 Адрес: {temp[2]}\n\n"
                           f'🙋‍♂️  {database.get("users", "name", callback.from_user.id)}\n'
                           f'👤 +{database.get("users", "phone", callback.from_user.id)} @{callback.from_user.username}\n\n'
                           f"📝 Источник: {temp[1]}\n"
                           f"▶️ <a href = '{temp[4]}'>Ссылка на объект</a>\n",
                           parse_mode='HTML')


@dp.callback_query(Text(text=root))
async def notif_turn_on(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)

    status = database.check_user(callback.from_user.id)
    if status < 1:
        await callback.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return
    temp = list(database.get('users', 'notif', callback.from_user.id))
    ind = root.index(callback.data)
    temp[ind] = ['1', '0'][int(temp[ind])]
    temp = ''.join(temp)

    await callback.message.edit_reply_markup(reply_markup=structure.make_settings(temp))
    await callback.answer(text=f"Уведомления о новых объектах на {callback.data} {['включены','отключены'][int(temp[ind])]}")
    database.edit_base(callback.from_user.id, 'users', 'notif', temp)


@dp.callback_query(Text(text=['take_work']))
async def take_work(callback: CallbackQuery):
    print(callback.from_user.username, callback.data)

    status = database.check_user(callback.from_user.id)
    if status < 1:
        await callback.answer(text='У вас нет доступа к боту', reply_markup=ReplyKeyboardRemove())
        return
    temp = database.get_object(callback.message.text.split('\n')[-1])
    if not temp:
        await callback.message.edit_text(text="Предложение не актуально\nОбъект уже взят в работу")
        return
    temp = database.get_work(callback.from_user.id, callback.message.text.split('\n')[-1])

    await callback.answer(text="Вы назначаны ответственным на данный объект")
    await callback.message.edit_text(text=f"✅ Вы взялись за объект \n{temp[4]}")
    await bot.send_message(chat_id=chat_id,
                           text=f"📍 Объект взят в работу агентом: \n🙋‍♂️ {database.get('users', 'name', callback.from_user.id)}\n"
                                f"👤 +{database.get('users', 'phone', callback.from_user.id)} @{callback.from_user.username}\n"
                                f"\n"
                                f"🔍 Название: {temp[3]}\n"
                                f"🧭 Адрес: {temp[2]}\n\n"
                                f"📝 Источник: {temp[1]}\n"
                                f"▶️ <a href = '{temp[4]}'>Ссылка на объект</a>", parse_mode='HTML')


@dp.message()
async def message(message: Message):  #
    print(message.chat.id)
    print(message.from_user.username, message.from_user.id, message.text)

    user_id = message.from_user.id
    status = database.check_user(message.from_user.id)

    if message.chat.id == message.from_user.id:
        if status == -1:  # Неизвестный пользователь
            return
        temp = message.text
        if status == 0:  # не зарегистрированный пользователь
            temp = temp.split('\n')

            if len(temp) != 2 or len(temp[0].split()) != 2:
                await message.answer(text='Неверный формат данных')
                return

            if not bool(re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                                 temp[1])):
                await message.answer(text='Неверный формат номера телефона')
                return

            database.second_reg(user_id, message.from_user.username, temp[0], temp[1])
            await message.answer(text='Вы успешно зарегистрированы!', reply_markup=structure.mainmenu_1)
            return
        func = database.get('users', 'using', message.from_user.id)
        if func == 0:
            await message.answer(text='Неизвестная команда!',reply_markup=structure.mainkeys[status])
            return

        if status == 1:  # обычный сотрудник
            if func == 1:
                database.set_func(message.from_user.id, '0')

                if 'cian' in message.text:
                    obj_id = message.text.split('/')[-2]
                elif 'avito' in message.text:
                    obj_id = message.text.split('?')[0][-10:]
                elif 'trk.mail' in message.text:
                    obj_id = message.text.split('=')[-1]
                elif 'youla' in message.text:
                    obj_id = message.text[-24:]
                elif 'mirkvartir' in message.text:
                    obj_id = message.text.split('/')[-2]
                else:
                    obj_id = 0
                print(obj_id)
                temp = database.check_obj(obj_id)
                if temp:
                    if temp[0][-1] == message.from_user.id:
                        await message.answer(text='Вы уже взялись за этот объект')
                        return
                    await message.answer(
                        text=f"📍 Этот объект уже взят в работу агентом \n🙋‍♂️ {database.get('users', 'name', temp[0][-1])}\n"
                             f"👤 +{database.get('users', 'phone', temp[0][-1])} @{database.get('users', 'username', temp[0][-1])}")
                    return
                await bot.send_message(chat_id=chat_id,
                                       text=f"📍 Объект взят в работу агентом: \n🙋‍♂️ {database.get('users', 'name', message.from_user.id)}\n"
                                            f"👤 +{database.get('users', 'phone', message.from_user.id)} @{message.from_user.username}\n"
                                            f"\n"
                                            f"▶️ <a href = '{message.text}'>Ссылка на объект</a>",
                                       parse_mode='HTML')
                await message.answer(text='Вы успешно взялись за объект')
                database.fast_work(obj_id, message.text, message.from_user.id)

        if status == 2:  # админ
            if func == 2:  # добавление номеров
                flag = False
                temp = message.text.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                for number in temp.split('\n'):
                    if bool(re.match(
                            r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                            number)):
                        print('g')
                        flag = True
                        database.new_number(number)

                if flag:
                    await message.answer(text="Номер(а) успешно добавлен(ы) в базу", reply_markup=structure.mainmenu_2)
                    database.set_func(message.from_user.id, 0)

    else:
        database.first_reg(message.from_user.id)
        if message.left_chat_member:
            database.remove_user(message.left_chat_member.id)


if __name__ == '__main__':
    dp.run_polling(bot)  # Запуск бота

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)

root = ['Циан', 'Юла', "Авито", 'Мир Квартир', 'Яндекс.Недвижимость']

notif_on: InlineKeyboardButton = InlineKeyboardButton(
    text='✅ Включить уведомления',
    callback_data='notif_turn_on')

notif_off: InlineKeyboardButton = InlineKeyboardButton(
    text='❌ Отключить уведомления',
    callback_data='notif_turn_off')


def make_settings(notifs):
    temp = [[InlineKeyboardButton(
        text=f'❌ {service} уведомления',
        callback_data=service),
        InlineKeyboardButton(
            text=f'✅ {service} уведомления',
            callback_data=service)]for service in root]
    return InlineKeyboardMarkup(inline_keyboard=[[temp[i][int(notifs[i])]] for i in range(5)])


take_work: InlineKeyboardButton = InlineKeyboardButton(
    text='✅ Взять объект в работу',
    callback_data='take_work')
take_work_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[take_work]])

cancel_but = InlineKeyboardButton(
    text="❌ Отмена",
    callback_data='cancel')
cancel = InlineKeyboardMarkup(inline_keyboard=[[cancel_but]])

delete_obj = InlineKeyboardButton(
    text='🗑️ Отказаться от объекта',
    callback_data='delete_obj'
)
obj_keys = InlineKeyboardMarkup(inline_keyboard=[[delete_obj]])


def set_page_but(now):
    next_obj = InlineKeyboardButton(
        text='➡️',
        callback_data=now
    )
    prev_obj = InlineKeyboardButton(
        text='⬅️',
        callback_data='-' + now
    )
    edit_obj = InlineKeyboardButton(
        text='✏️ Изменить',
        callback_data='edit_obj'
    )
    return InlineKeyboardMarkup(inline_keyboard=[[prev_obj, edit_obj, next_obj]])


number_but = KeyboardButton(text="🤳 Получить номер для прозвона")
help_but = KeyboardButton(text='❔ Помощь')
settings_butt = KeyboardButton(text='⚙️ Настройки')
add_number = KeyboardButton(text='➕ Добавить номер для прозвона')
my_objects = KeyboardButton(text='🏢 Мои объекты')
take_object = KeyboardButton(text='🧭 Взяться за объект по ссылке')

# remove_user = KeyboardButton(text='✅ Добавить пользователя')

mainmenu_1 = ReplyKeyboardMarkup(keyboard=[[number_but], [take_object], [my_objects, settings_butt]],
                                 resize_keyboard=True)
mainmenu_2 = ReplyKeyboardMarkup(keyboard=[[settings_butt, help_but], [add_number]],
                                 resize_keyboard=True)

mainkeys = ['', mainmenu_1, mainmenu_2]
help_text = ["Пункт помощь"]

if __name__ == '__main__':
    print(make_settings('11111'))

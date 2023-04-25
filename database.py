import sqlite3

con = sqlite3.connect('database.db')
cursorObj = con.cursor()


def get(table, part, id):
    return cursorObj.execute(f'SELECT "{part}" FROM "{table}" WHERE id = {id}').fetchall()[0][0]


def check_user(id):  # сотрудник ли это
    try:
        return cursorObj.execute(f"SELECT lvl FROM users WHERE id = {id}").fetchall()[0][0]
    except IndexError:
        return -1


def get_user_ob(id):
    return cursorObj.execute(f"SELECT * FROM objects WHERE response = {id}").fetchall()


def all_work_ob():
    try:
        return [str(i[0]) for i in cursorObj.execute('SELECT id FROM objects WHERE status != 0').fetchall()]
    except IndexError:
        return []


def first_reg(id):
    if (id,) in cursorObj.execute(f"SELECT id FROM users").fetchall():
        return
    cursorObj.execute(f'INSERT INTO users (id, lvl) VALUES{(id, 0)}')
    con.commit()


def second_reg(id, username, name, phone):
    cursorObj.execute(f"DELETE FROM users WHERE id = {id}")

    cursorObj.execute(
        f'INSERT INTO users ("id", "username", "name", "phone", "lvl", "notif", "using") VALUES{(id, username, name, phone, 1, "00000", 0)}')
    con.commit()


def remove_user(id):
    cursorObj.execute(f"DELETE FROM users WHERE id = {id}")

    con.commit()


def new_object(id, service, address, name, url):
    if cursorObj.execute(f'SELECT id FROM objects WHERE id = "{id}"').fetchall():
        return False
    cursorObj.execute(
        f"INSERT INTO objects (id, service, address, name, url, status, response) VALUES{(id, service, address, name, url, 0, 0)}")
    con.commit()
    return True


def edit_base(id, table, part, change):
    cursorObj.execute(f'UPDATE {table} SET {part} = "{change}" where id = {id}')

    con.commit()


def notif_users():
    all_notif = {i[0]: i[5] for i in cursorObj.execute("SELECT * FROM users WHERE notif != '00000'").fetchall()}

    result = [[], [], [], [], []]
    for user in all_notif:
        for notif in range(5):
            if all_notif[user][notif] == '1':
                result[notif].append(user)

    return result


def get_object(id):
    temp = cursorObj.execute(f'SELECT * FROM objects WHERE id = "{id}" AND status = 0').fetchall()
    if not temp:
        return []
    return temp[0]


def get_work(user_id, id):
    cursorObj.execute(f'UPDATE objects SET status = 1 WHERE id = "{id}"')
    cursorObj.execute(f'UPDATE objects SET response = {user_id} WHERE id = "{id}"')

    con.commit()
    return cursorObj.execute(f'SELECT * FROM objects WHERE id = "{id}"').fetchall()[0]


def new_number(number):
    cursorObj.execute(f"INSERT INTO phones(number) VALUES({number})")
    con.commit()


def get_number():
    temp = [i[0] for i in cursorObj.execute('SELECT number FROM phones').fetchall()]
    if temp:
        cursorObj.execute(f"DELETE FROM phones WHERE number = {temp[-1]}")
        con.commit()

        return temp[-1]
    return -1


def set_func(id, func):
    cursorObj.execute(f'UPDATE users SET "using" = {func} WHERE id = {id}')
    con.commit()


def pages(id, now):
    if '-' in now:
        now = abs(int(now)) - 1
    else:
        now = int(now) + 1
    temp = len(cursorObj.execute(f'SELECT * FROM objects WHERE response = {id}').fetchall())
    if temp == 0:
        return False
    if now < 0:
        now = temp - 1
    else:
        now %= temp
    return get_user_ob(id)[now], str(now)


def delete_obj(user_id, obj_id):
    temp = cursorObj.execute(f'SELECT * FROM objects WHERE id = {obj_id} AND response = {user_id}').fetchall()
    if not temp:
        return
    cursorObj.execute(f"UPDATE objects SET status = 0 WHERE id = {obj_id}")
    cursorObj.execute(f"UPDATE objects SET response = 0 WHERE id = {obj_id}")
    con.commit()
    return temp


def check_obj(id):
    return cursorObj.execute(f'SELECT * FROM objects WHERE id = "{id}" AND status != 0').fetchall()


def fast_work(id, url, response):
    if cursorObj.execute(f'SELECT id FROM objects WHERE id = "{id}"').fetchall():
        cursorObj.execute(f'UPDATE objects SET status = 1 WHERE id = "{id}"')
        cursorObj.execute(f'UPDATE objects SET response = {response} WHERE id = "{id}"')
        con.commit()
        return
    cursorObj.execute(
        f"INSERT INTO objects(id, service, address, name, url,status,response) VALUES{(id, 'Неизвестен', 'Неизвестен', 'Неизвестно', url, 1, response)}")

    con.commit()


if __name__ == '__main__':
    # new_object(1, 2, 3, 4, 5)
    # print(get_object(285053080))
    # print(pages(1132908805, '2'))
    # fast_work(55, 'sdsd1', 5)
    print(notif_users())
    pass

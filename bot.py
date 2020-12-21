import psycopg2
import telebot;
from telebot import types
bot = telebot.TeleBot('1437332614:AAH7E_wv6UouGOYGkEaSEMusevrRwkAbiqM');

fields_to_update = []
data_to_update = []
fields = {
    'managers': '(firstname, surname, phone_number, orders_closed)',
    'customers': '(firstname, surname, phone_number, city, street, email)',
    'items': '(cost, articul, id_manager)',
    'order_item': '(amount, id_order, id_item)',
    'orders': '(created_time, payment_time, total_cost, is_finished, id_customer, id_manager)',
    'storage_items': '(amount, id_storage, id_item)',
    'storages': '(city, street, capacity, avialable_place)',
    'yarn': '',
    'goods': '',
    }
name = '';
password = '';
conn = None
cur = None

action = ''
table = ''
id_item = ''
data = ''

def make_sql(text):
    try:
        cur.execute(text)
        query_results = cur.fetchall()
        text = '\n\n'.join([' | '.join(map(str, x)) for x in query_results])
        if len(text) < 3:
            return 'Выполнил запрос.'
        return text
    except Exception as e:
        print(e)
        return 'Произошла какая-то ошибка: ' + str(e)

def checker(str):
    if str.isnumeric():
        return str
    return "'" + str.strip() + "'"

def update_data():
    print('fields : ', fields_to_update, '\ndata: ', data_to_update, '\ntable: ', table, '\nid:', id_item)
    try:
        params = ''
        for i in range(len(data_to_update)):
            params += str(fields_to_update[i]) + '=' +  checker(str(data_to_update[i])) + ','
        print('UPDATE ' + table + ' SET ' + params[0:-1] + ' WHERE id_' + table[0:-1] + ' = ' + id_item)
        cur.execute('UPDATE ' + table + ' SET ' + params[0:-1] + ' WHERE id_' + table[0:-1] + ' = ' + id_item + ';')
        return 'Обновление прошло успешно'
    except Exception as e:
        print(e)
        return 'Произошла какая-то ошибка: ' + str(e)

def insert_data():
    global fields
    try:
        cur.execute('INSERT INTO ' + table  + ' ' + fields[table] + ' VALUES ' + data+ ';')
        return 'Успешно вставили данные'
    except Exception as e:
        print(e)
        return 'Произошла какая-то ошибка: ' + str(e)

def get_data_by_id():
    try:
        if action == 'storage-items':
            cur.execute('SELECT * FROM ' + 'get_storage_items(' + id_item + ')'+ ';')
        elif action == 'order-items':
            cur.execute('SELECT * FROM ' + 'get_order_items(' + id_item + ')'+ ';')
        elif action == 'count-items':
            cur.execute('SELECT * FROM ' + 'count_item_everywhere(' + id_item + ')'+ ';')
        elif action == 'sold-by-manager':
            cur.execute('SELECT * FROM ' + 'items_sold_by_manager ()')
        elif action == 'sold-items':
            cur.execute('SELECT * FROM ' + 'items_sold ()')
        else:
            cur.execute("SELECT * FROM " + table + ' WHERE id_' + table[0:-1] + ' = ' + id_item+ ';')
        query_results = cur.fetchall()
        text = '\n\n'.join([' | '.join(map(str, x)) for x in query_results])
        if len(text) < 3:
            return 'По данному запросу ничего не нашлось'
        return text
    except Exception as e:
        print(e)
        return 'Произошла какая-то ошибка: ' + str(e)

def get_data_all():
    try:
        cur.execute("SELECT * FROM " + table+ ';')
        query_results = cur.fetchall()
        text = '\n\n'.join([' | '.join(map(str, x)) for x in query_results])
        if len(text) < 3:
            return 'По данному запросу ничего не нашлось'
        return text
    except Exception as e:
        print(e)
        return 'Произошла какая-то ошибка: ' + str(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global action
    global table
    global item_id
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Отлично! Сейчас я попробую авторизировать тебя...');
        try:
            global conn
            global cur
            conn = psycopg2.connect(
            host='localhost',
            database='ESM',
            user=name,
            password=password
            )
            cur = conn.cursor()
            bot.send_message(call.message.chat.id, 'Логин и пароль верный, работаем!');
            keyboard = types.InlineKeyboardMarkup();
            key_req = types.InlineKeyboardButton(text='Запросы к базе', callback_data='requests'); 
            keyboard.add(key_req); 
            key_special= types.InlineKeyboardButton(text='Отчеты', callback_data='special');
            keyboard.add(key_special);
            key_custom= types.InlineKeyboardButton(text='Кастомные запросы к базе на SQL', callback_data='custom');
            keyboard.add(key_custom);
            question = 'Чем бы вы хотели сейчас заняться?';
            bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            bot.send_message(call.message.chat.id, 'Произошла ошибка :' + str(error));
        except:
            bot.send_message(call.message.chat.id, 'Произошла ошибка :');
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Тогда введи \reg еще раз :)');
    elif call.data == "requests":
        keyboard = types.InlineKeyboardMarkup();
        key_select = types.InlineKeyboardButton(text='Выбрать', callback_data='select-req'); 
        keyboard.add(key_select); 
        key_update= types.InlineKeyboardButton(text='Обновить значения', callback_data='update-req');
        keyboard.add(key_update);
        key_insert= types.InlineKeyboardButton(text='Добавить запись', callback_data='insert-req');
        keyboard.add(key_insert);
        question = 'Какой запрос?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == "select-req":
        action = 'select'
        keyboard = types.InlineKeyboardMarkup(row_width=3);
        key_managers = types.InlineKeyboardButton(text='Работники', callback_data='s-managers'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Покупатели', callback_data='s-customers');
        keyboard.add(key_customers);
        key_items= types.InlineKeyboardButton(text='Товары', callback_data='s-items');
        keyboard.add(key_items);
        key_storages= types.InlineKeyboardButton(text='Склады', callback_data='s-storages');
        keyboard.add(key_storages);
        key_orders= types.InlineKeyboardButton(text='Заказы', callback_data='s-orders');
        keyboard.add(key_orders);
        question = 'Из какой таблицы берем данные?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 's-managers':
        table = 'managers'
        keyboard = types.InlineKeyboardMarkup(row_width=2);
        key_managers = types.InlineKeyboardButton(text='Id', callback_data='s-st-id'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Все данные', callback_data='s-st-all');
        keyboard.add(key_customers);
        question = 'Все данные или по id?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 's-customers':
        table = 'customers'
        keyboard = types.InlineKeyboardMarkup(row_width=2);
        key_managers = types.InlineKeyboardButton(text='Id', callback_data='s-st-id'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Все данные', callback_data='s-st-all');
        keyboard.add(key_customers);
        question = 'Все данные или по id?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 's-items':
        table = 'items'
        keyboard = types.InlineKeyboardMarkup(row_width=2);
        key_managers = types.InlineKeyboardButton(text='Id', callback_data='s-st-id'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Все данные', callback_data='s-st-all');
        keyboard.add(key_customers);
        question = 'Все данные или по id?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 's-orders':
        table = 'orders'
        keyboard = types.InlineKeyboardMarkup(row_width=2);
        key_managers = types.InlineKeyboardButton(text='Id', callback_data='s-st-id'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Все данные', callback_data='s-st-all');
        keyboard.add(key_customers);
        question = 'Все данные или по id?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 's-storages':
        table = 'storages'
        keyboard = types.InlineKeyboardMarkup(row_width=2);
        key_managers = types.InlineKeyboardButton(text='Id', callback_data='s-st-id'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Все данные', callback_data='s-st-all');
        keyboard.add(key_customers);
        question = 'Все данные или по id?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 's-st-all':
        text = get_data_all()
        bot.send_message(call.message.chat.id, text=text)
    elif call.data == 's-st-id':
        bot.send_message(call.message.chat.id, 'Введите id')
        bot.register_next_step_handler(call.message, get_id);
    elif call.data == "update-req":
        action = 'update'
        keyboard = types.InlineKeyboardMarkup(row_width=3);
        key_managers = types.InlineKeyboardButton(text='Работники', callback_data='u-managers'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Покупатели', callback_data='u-customers');
        keyboard.add(key_customers);
        key_items= types.InlineKeyboardButton(text='Товары', callback_data='u-items');
        keyboard.add(key_items);
        key_storages= types.InlineKeyboardButton(text='Склады', callback_data='u-storages');
        keyboard.add(key_storages);
        key_orders= types.InlineKeyboardButton(text='Заказы', callback_data='u-orders');
        keyboard.add(key_orders);
        question = 'В какой таблице обновим значения?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 'u-managers':
        table = 'managers'
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: Имя, Фамилия, обработал заказов)";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields); 
    elif call.data == "u-customers":
        table = "customers"
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: Имя, Фамилия, Город, Улица, email";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields);
    elif call.data == "u-items":
        table = "items"
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: Цена, Артикул, id менеджера";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields);
    elif call.data == "u-orders":
        table = "orders"
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: оплачен, завершен";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields);
    elif call.data == "u-storages":
        table = "storages"
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: Город, улица";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields);
    elif call.data == "u-order_items":
        table = "order_item"
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: сколько товара";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields);
    elif call.data == "u-storage_items":
        table = "storage_item"
        question = "Введите через запятую название полей, которые хотите изменить, доступные поля: сколько товара";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_fields);
    elif call.data == "insert-req":
        action = 'insert'
        keyboard = types.InlineKeyboardMarkup(row_width=3);
        key_managers = types.InlineKeyboardButton(text='Работники', callback_data='i-managers'); 
        keyboard.add(key_managers); 
        key_customers= types.InlineKeyboardButton(text='Покупатели', callback_data='i-customers');
        keyboard.add(key_customers);
        key_items= types.InlineKeyboardButton(text='Товары', callback_data='i-items');
        keyboard.add(key_items);
        key_storages= types.InlineKeyboardButton(text='Склады', callback_data='i-storages');
        keyboard.add(key_storages);
        key_orders= types.InlineKeyboardButton(text='Заказы', callback_data='i-orders');
        keyboard.add(key_orders);
        key_ord_it= types.InlineKeyboardButton(text='Товар-заказ', callback_data='i-order_items');
        keyboard.add(key_ord_it);
        key_sto_it= types.InlineKeyboardButton(text='Товар-склад', callback_data='i-storage_items');
        keyboard.add(key_sto_it);
        question = 'Из какой таблицы берем данные?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 'i-managers':
        table = 'managers'
        question = "Введите данные для вставки в формате ('Имя', 'Фамилия', Номер телефона, 0), ('Имя', 'Фамилия', Номер телефона, 0), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "i-customers":
        table = "customers"
        question = "Введите данные для вставки в формате ('Имя', 'Фамилия', Номер телефона, 'Город', 'Улица', 'email'), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "i-items":
        table = "items"
        question = "Введите данные для вставки в формате (Цена, 'Артикул', id менеджера), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "i-orders":
        table = "orders"
        question = "Введите данные для вставки в формате (создан: дд-мм-гг, оплачен: дд-мм-гг, 0, завершен (1/0), id покупателя, id менеджера), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "i-storages":
        table = "storages"
        question = "Введите данные для вставки в формате ('Город', 'улица', вместимость, свободно места), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "i-order_items":
        table = "order_item"
        question = "Введите данные для вставки в формате (сколько товара, id заказа, id товара), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "i-storage_items":
        table = "storage_item"
        question = "Введите данные для вставки в формате (сколько товара, id склада, id товара), (...), ...";
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_insert);
    elif call.data == "special":
        keyboard = types.InlineKeyboardMarkup();
        key_si = types.InlineKeyboardButton(text='Получить список товаров со склада', callback_data='storage-items'); 
        keyboard.add(key_si); 
        key_oi= types.InlineKeyboardButton(text='Получить список товаров в заказе', callback_data='order-items');
        keyboard.add(key_oi); 
        key_сi= types.InlineKeyboardButton(text='Посчитать количество товара по всем складам', callback_data='count-items');
        keyboard.add(key_сi);
        key_sii= types.InlineKeyboardButton(text='Сколько единиц товаров продано', callback_data='sold-items');
        keyboard.add(key_sii);
        key_sibm= types.InlineKeyboardButton(text='Число проданных товаров, добавленных каждым из менеджеров', callback_data='sold-by-manager');
        keyboard.add(key_sibm);
        question = 'Какой из запросов?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == 'storage-items':
        action = call.data
        question = 'Введите id склада';
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_id);
    elif call.data == 'sold-by-manager':
        action = call.data
        question = get_data_by_id()
        bot.send_message(call.message.chat.id, text=question)
    elif call.data == 'sold-items':
        action = call.data
        question = get_data_by_id()
        bot.send_message(call.message.chat.id, text=question)
    elif call.data == 'order-items':
        action = call.data
        question = 'Введите id заказа';
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_id);
    elif call.data == 'count-items':
        action = call.data
        question = 'Введите id товара';
        bot.send_message(call.message.chat.id, text=question)
        bot.register_next_step_handler(call.message, get_id);
    elif call.data == "custom":
        text = 'Введи запрос на SQL. Каждый запрос - на новой строке, раздели запросы ;.'
        bot.send_message(call.message.chat.id, text=text)
        bot.register_next_step_handler(call.message, sql_handler);



@bot.message_handler(content_types=['text'])
def start(message):
    print(message.text)
    if message.text == '/reg' or name == '' or password == '':
        bot.send_message(message.from_user.id, "Сейчас ты будешь тестировать функционал бота. Я спрошу у тебя логин и пароль для доступа к данным, ты можешь ввести user1 с паролем 226104 чтобы войти и протестировать. \nВведи свой username.");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    elif message.text == '/close':
        conn.close()
        bot.send_message(message.from_user.id, 'Закрыли соединение с базой.');
    elif message.text == '/new':
        keyboard = types.InlineKeyboardMarkup();
        key_req = types.InlineKeyboardButton(text='Запросы к базе', callback_data='requests'); 
        keyboard.add(key_req); 
        key_special= types.InlineKeyboardButton(text='Отчеты', callback_data='special');
        keyboard.add(key_special);
        key_custom= types.InlineKeyboardButton(text='Кастомные запросы к базе на SQL', callback_data='custom');
        keyboard.add(key_custom);
        question = 'Чем бы вы хотели сейчас заняться?';
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif name != '':
        bot.send_message(message.from_user.id, 'Напиши /new чтобы выполнить еще запрос или получить отчет');
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
    global name
    name = message.text;
    bot.send_message(message.from_user.id, 'Пароль для доступа к БД?');
    bot.register_next_step_handler(message, get_password);


def get_password(message):
    global password
    password = message.text;
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Логин '+ name + '\nПароль ' + password+ '\nВсе верно?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def get_id(message):
    print('i was called')
    global id_item
    if (message.text.isnumeric() or message.text[0] != '/'):
        id_item = message.text  
        text = get_data_by_id()
        bot.send_message(message.from_user.id, text=text)

def get_insert(message):
    global data
    data = message.text
    text = insert_data()
    bot.send_message(message.from_user.id, text=text)

def translate(field):
    if field == 'имя':
        return 'firstname'
    elif field == 'фамилия':
        return 'surname'
    elif field == 'обработал заказов':
        return 'orders_closed'
    elif field == 'город':
        return 'city'
    elif field == 'улица':
        return 'street'
    elif field == 'email':
        return 'email'
    elif field == 'цена':
        return 'price'
    elif field == 'артикул':
        return 'articul'
    elif field == 'id менеджера':
        return 'id_manager'
    elif field == 'оплачен':
        return 'payment_time'
    elif field == 'завершен':
        return 'isFinished'
    elif field == 'сколько товара':
        return 'amount'

def get_fields(message):
    global fields_to_update
    data = message.text.split(',')
    data_tr = []
    for i in range(len(data)):
        data_tr.append(translate(data[i].lower().strip()))
    fields_to_update = data_tr
    bot.send_message(message.from_user.id, text='Введите значения, которые хотите вставить в эти поля через запятую')
    bot.register_next_step_handler(message, get_updated);

def get_updated(message):
    global data_to_update
    data = message.text.split(',')
    data_to_update = data
    bot.send_message(message.from_user.id, text='Введите id объекта, у которого вы хотите обновить значения')
    bot.register_next_step_handler(message, get_id_upd);

def get_id_upd(message):
    global id_item
    id_item = message.text
    text = update_data()
    bot.send_message(message.from_user.id, text=text)

def sql_handler(message):
    text = make_sql(message.text)
    bot.send_message(message.from_user.id, text=text)
bot.polling(none_stop=True, interval=0)
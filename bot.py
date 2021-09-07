import telebot 
import pymongo
import config


db_client = pymongo.MongoClient("mongodb://localhost:27017/")
current_db = db_client["razmanov_admin"]
collection = current_db["users"]
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def main(message):
    status = 'no answer'
    bot.send_message(message.chat.id, text="Ура, я заработал")
    userdb = create_userdb(message, status)
    save_user_data(message, userdb)
    # show_usersdb(collection)
    task_for_user(message)


def save_user_data(message, userdb):
    if collection.count_documents({'chat_id': message.chat.id}) > 0:
        if not message.from_user.username:
            if collection.find_one({'chat_id': message.chat.id, 'status': 'True result'}):
                bot.send_message(message.chat.id, text='Привет, ' + message.from_user.first_name + ', я тебя помню! Последний раз ответил')
                update_userdb(message, userdb)
        elif message.from_user.username != 'first_telegram66345_bot':
            if collection.find_one({'chat_id': message.chat.id, 'status': 'True result'}):
                bot.send_message(message.chat.id, text='Привет, ' + message.from_user.first_name + ', я тебя помню! Последний раз ответил')
                update_userdb(message, userdb)
    else:
        insert_result = collection.insert_one(userdb)
        print('New user: \n')
        print(insert_result.inserted_id)


def update_userdb(message, userdb):
    print("User " + str(message.chat.id) + " data update")
    collection.update_one({'chat_id': message.chat.id}, {'$set': userdb})


def create_userdb(message, status):
    if not message.from_user.username:
        username = 'None'
    else:
        username = message.from_user.username
    if not message.from_user.last_name:
        last_name = 'None'
    else:
        last_name = message.from_user.last_name
    if not message.from_user.first_name:
        first_name = 'None'
    else:
        first_name = message.from_user.first_name
    # status = 
    userdb = {
        'chat_id': message.chat.id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'status': status
    }
    return userdb


def task_for_user(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='200', callback_data='200'))
    markup.add(telebot.types.InlineKeyboardButton(text='300', callback_data='300'))
    markup.add(telebot.types.InlineKeyboardButton(text='400', callback_data='400'))
    bot.send_message(message.chat.id, text="Сколько будет 150 + 150?", reply_markup=markup)


def show_usersdb(show_collection):
    print('Users:')
    for user in (show_collection.find().sort('username')):
        print('id: ' + str(user["chat_id"]) + '\t username: ' + user['username'] + '\t Name: ' + user['first_name']
                                            + ' ' + user['last_name'] + ' ' + user['status'])


def ask_user(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Да', callback_data='1'))
    markup.add(telebot.types.InlineKeyboardButton(text='Нет', callback_data='0'))
    bot.send_message(message.chat.id, text="Хочешь попробовать еще раз?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: int(call.data) > 1)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Ответ принят!')
    if call.data == '300':
        answer = 'Ну, ты сам знаешь кто твой любовник...'
        status = 'True result'
    else:
        answer = 'Плохо, пробуй еще! @Drow_Ranger'
        status = 'False result'
    save_user_data(call.message, create_userdb(call.message, status))
    bot.send_message(call.message.chat.id, answer)
    ask_user(call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('1'))
def callback_repeat(call):
    bot.answer_callback_query(callback_query_id=call.id, text='ОКЕЙ!')
    task_for_user(call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('0'))
def callback_repeat(call):
    answer = 'Ладно, в следующий раз!'
    bot.send_message(call.message.chat.id, answer)
    


bot.polling()

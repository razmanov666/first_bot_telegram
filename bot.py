import re
import telebot
import json
import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
current_db = db_client["razmanov_admin"]
collection = current_db["users"]

bot = telebot.TeleBot("1827098555:AAFay8gZy4c5pyxUc6I3HpkOgeheDl63Tww")


@bot.message_handler(commands=['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, text="Ура, я заработал")
    userdb = create_userdb(message)
    insert_result = collection.insert_one(userdb)
    print(insert_result.inserted_id)
    # with open('users.json', 'r') as read_users:
    #     read_data = json.load(read_users)
    #     read_users.close()

    # if len(read_data) >= 1:
    #     result = json.dumps(read_data)
    #     result = re.sub(r'}$', ',', result)
    #     create_user(result, read_data, message)
    task_for_user(message)


def create_userdb(message):
    userdb = {
        'chat_id': message.chat.id,
        'username': 'asd',
        'first_name': 'asdasd',
        'last_name': 'asddaadsddas',
        'status': 'reg'
    }
    return userdb


def task_for_user(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='200', callback_data='200'))
    markup.add(telebot.types.InlineKeyboardButton(text='300', callback_data='300'))
    markup.add(telebot.types.InlineKeyboardButton(text='400', callback_data='400'))
    bot.send_message(message.chat.id, text="Сколько будет 150 + 150?", reply_markup=markup)


def create_user(result, read_data, message):
    # bot.send_message(message.chat.id, text="Ура, я заработал")
    # print((result + '"user' + str(len(read_data) + 1) + '": [{"chat_id": "' + str(message.chat.id) + '",' +
    #                        '"username": "' + message.from_user.username + '",' +
    #                        '"first_name": "' + message.from_user.first_name + '",' +
    #                        '"last_name": "' + message.from_user.last_name + '",' +
    #                        '"status": "reg12142"}]}'))
    parse = check_user_in_json(read_data, message)
    user_data = get_user_data(result, read_data, message)
    if parse:
        print('parse: OK')
        with open('users.json', 'w', encoding='utf-8') as users:
            json.dump(user_data, users, ensure_ascii=False, indent=4)
    else:
        bot.send_message(message.chat.id, text='Привет, ' + message.from_user.first_name + ', я тебя помню!')


def check_user_in_json(read_data, message):
    parse = True
    user_list = range(1, len(read_data) + 1)
    for i in user_list:
        for user in read_data["user" + str(i)]:
            for k, v in user.items():
                if k == 'chat_id' and v == str(message.chat.id):
                    if message.from_user.username:
                        print('parse: already exist' + '\nUsername: ' + message.from_user.username)
                    elif message.from_user.last_name:
                        name = message.from_user.first_name + message.from_user.last_name
                        print('parse: already exist' + '\nName: ' + name)
                    else:
                        print('parse: already exist' + '\nName: ' + message.from_user.first_name)
                    print('K = ' + str(message.chat.id))
                    parse = False
                    break
    return parse


def get_user_data(result, read_data, message):
    if message.from_user.last_name:
        last_name = message.from_user.last_name
    else:
        last_name = ''
    if message.from_user.username:
        username = message.from_user.username
    else:
        username = ''
    user_data = (result + '"user' + str(len(read_data) + 1) + '": [{"chat_id": "' + str(message.chat.id) + '",' +
                 '"username": "' + username + '",' +
                 '"first_name": "' + message.from_user.first_name + '",' +
                 '"last_name": "' + last_name + '",' +
                 '"status": "reg12142"}]}')

    return json.loads(user_data)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Ответ принят!')
    if call.data == '300':
        answer = 'Ну, ты сам знаешь кто твой любовник...'
    else:
        answer = 'Плохо, пробуй еще! @Drow_Ranger'
    bot.send_message(call.message.chat.id, answer)


bot.polling()

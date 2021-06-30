import re
import telebot
import json

bot = telebot.TeleBot("1827098555:AAFay8gZy4c5pyxUc6I3HpkOgeheDl63Tww")


@bot.message_handler(commands=['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, text="Ура, я заработал")
    try:
        read_data = get_users(message)
        bot.send_message(message.chat.id, text='Привет, ' + message.from_user.first_name + ', я тебя помню!')
        print('exists')
    except FileNotFoundError:
        create_user(message)
        read_data = get_users(message)
    update_user_status('NEW_STATUS', message)
    task_for_user(message)


def get_users(message):
    with open('users/' + str(message.chat.id) + '.json') as read_users:
        read_data = json.load(read_users)
        read_users.close()
    return read_data


def task_for_user(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='200', callback_data='200'))
    markup.add(telebot.types.InlineKeyboardButton(text='300', callback_data='300'))
    markup.add(telebot.types.InlineKeyboardButton(text='400', callback_data='400'))
    bot.send_message(message.chat.id, text="Сколько будет 150 + 150?", reply_markup=markup)


def create_user(message):
    user_data = get_user_data(message)
    print('parse: OK')
    write_user_data(user_data, message)
    update_user_status('NEW_STATUS', message)


def write_user_data(user_data, message):
    try:
        with open('users/' + str(message.chat.id)+'.json', 'x', encoding='utf-8') as users:
            json.dump(user_data, users, ensure_ascii=False, indent=4)
    except FileExistsError:
        with open('users/' + str(message.chat.id)+'.json', 'w', encoding='utf-8') as users:
            json.dump(user_data, users, ensure_ascii=False, indent=4)
    finally:
        print('OK')


# def check_user_in_json(read_data, message):
#     try:
#         reading_data = read_data[str(message.chat.id)]
#         if message.from_user.username:
#             print('parse: already exist' + '\nUsername: ' + message.from_user.username)
#         elif message.from_user.last_name:
#             name = message.from_user.first_name + message.from_user.last_name
#             print('parse: already exist' + '\nName: ' + name)
#         else:
#             print('parse: already exist' + '\nName: ' + message.from_user.first_name)
#             print('K = ' + str(message.chat.id))
#         return False
#     except KeyError:
#         return True


def get_user_data(message):
    if message.from_user.last_name:
        last_name = message.from_user.last_name
    else:
        last_name = ''
    if message.from_user.username:
        username = message.from_user.username
    else:
        username = ''
    user_data = ('{"' + str(message.chat.id) + '": { ' +
                 '"username": "' + username + '",' +
                 '"first_name": "' + message.from_user.first_name + '",' +
                 '"last_name": "' + last_name + '",' +
                 '"status": "reg12142"}}')

    return json.loads(user_data)


def update_user_status(status, message):
    read_data = get_users(message)
    new_user_data = read_data
    new_user_data[str(message.chat.id)]['status'] = status
    write_user_data(new_user_data, message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Ответ принят!')
    if call.data == '300':
        answer = 'Ну, ты сам знаешь кто твой любовник...'
    else:
        answer = 'Плохо, пробуй еще!'
    bot.send_message(call.message.chat.id, answer)


bot.polling()

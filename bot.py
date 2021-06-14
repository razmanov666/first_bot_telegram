import telebot

bot = telebot.TeleBot("1827098555:AAFay8gZy4c5pyxUc6I3HpkOgeheDl63Tww")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text="Ура, я заработал")
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Нет', callback_data='Нет'))
    markup.add(telebot.types.InlineKeyboardButton(text='Да', callback_data='Да'))
    markup.add(telebot.types.InlineKeyboardButton(text='300', callback_data='300'))
    bot.send_message(message.chat.id, text="Хочешь задачку?", reply_markup=markup)

    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton(text='300', callback_data=300))
    # markup.add(telebot.types.InlineKeyboardButton(text='400', callback_data=400))
    # markup.add(telebot.types.InlineKeyboardButton(text='500', callback_data=500))
    # bot.send_message(message.chat.id, text="Сколько будет 150+150?", reply_markup=markup)
    # bot.send_message(517020426, text="Я еще подумаю", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Ответ принят!')
    if call.data == '300':
        answer = 'Ну, ты сам знаешь кто твой любовник...'
    else:
        answer = 'Плохо, пробуй еще!'
    bot.send_message(call.message.chat.id, answer)


bot.polling()

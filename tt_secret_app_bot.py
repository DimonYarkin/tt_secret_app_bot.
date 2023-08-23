import telebot
from telebot import types

# t.me/tt_secret_app_bot
TOKEN = '6651199720:AAEDz5D_75THAwsrMR7IFajHeFbGsmIDys8'
bot = telebot.TeleBot(TOKEN)
ls_dict = {}


# Функция возвращает словарь каналов для регистрации
def get_chanels():
    dic_chan = {'https://t.me/anikdot_market': '@anikdot_market',
                'https://t.me/futbol_clubs': '@futbol_clubs',
                'https://t.me/new_chanel1_1': '@new_chanel1_1',
                'https://t.me/mmarket_place': '@mmarket_place',
                'https://t.me/topcash_game': '@topcash_game',

                }
    return dic_chan


def check_chat_member(user_id, TELEGRAM_CHANNEL_ID):
    try:
        member = bot.get_chat_member(TELEGRAM_CHANNEL_ID, user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            return False
        else:
            return True
    except:
        return False


def check_valide_chats(user_id):
    for key, value in get_chanels().items():
        if not check_chat_member(user_id, value):
            return False
    return True


# Функция возвращает заголовок рекламного сообщения
def get_handler():
    text_hand = '<b>Данное приложение является платным, но благодаря нашим спонсорам вы можете получить его совершенно бесплатно, вам нужно лишь подписаться на всех спонсоров и нажать кнопку «проверить подписку» :</b>⬇️'
    return text_hand


def get_message_sponsor(message):
    global ls_dict
    markup = types.InlineKeyboardMarkup()
    for key, value in get_chanels().items():
        btn_sp = types.InlineKeyboardButton(text=value, callback_data='btn', url=key)
        markup.add(btn_sp)
    ls_dict[message.chat.id].append(
        bot.send_message(message.chat.id, get_handler(), parse_mode='html', reply_markup=markup).id)

    markup1 = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(text="Проверить подписку", callback_data='end')
    markup1.add(btn2)
    ls_dict[message.chat.id].append(
        bot.send_message(message.chat.id, "🚫 Отписываться от спонсоров нельзя, иначе скачивание будет недоступно",
                         reply_markup=markup1).id)


# Обработка действий при старте
@bot.message_handler(commands=['start'])
def main(message):
    global ls_dict
    ls_dict[message.chat.id] = []

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Продолжить", callback_data='recept')
    markup.add(btn1)
    ls_dict[message.chat.id].append(
        bot.send_message(message.chat.id,
                         "<b>Привет</b> 👋  \n В этом боте ты сможешь скачать то самое приложение из тт \n Жми «продолжить», чтобы получить приложение 🤫",
                         parse_mode='html', reply_markup=markup).id)
    # ls_dict[message.chat.id].append(bot.send_message(message.chat.id, "Выбери рецепт", reply_markup=markup).id)


# Обработка кал бэк функцин нажатия на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global ls_ms, ls_dict
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == "recept":
        get_message_sponsor(call.message)

    if call.data == "end":
        if not check_valide_chats(call.from_user.id):
            for ls in ls_dict[call.message.chat.id]:
                try:
                    bot.delete_message(call.message.chat.id, ls)
                except Exception as e:
                    pass
            ls_dict[call.message.chat.id] = []
            ls_dict[call.message.chat.id].append(
                bot.send_message(call.message.chat.id,
                                 "К сожалению, вы не подписаны на всех спонсоров 😔 <b>, подпишитесь, чтобы получить приложение: </b>",
                                 parse_mode='html').id)

            get_message_sponsor(call.message)
        else:
            for ls in ls_dict[call.message.chat.id]:
                try:
                    bot.delete_message(call.message.chat.id, ls)
                except Exception as e:
                    pass
            ls_dict.pop(call.message.chat.id)
            strms = "<b>Готово!</b> ✅ \n \n"
            strms += "Наши менеджеры активно занимаются проверкой твоей \n"
            strms += "подписки на спонсоров, приносим извинения за ожидание ❤️ \n \n"
            strms += "‼️<b>Как только проверка будет закончена, файл будет</b> \n"
            strms += "<b>отправлено сюда</b> ‼️\n \n"
            strms += "🚫Во время ожидания нельзя отписываться от каналов \n"
            strms += "спонсоров, иначе отправка не произойдет. \n"


            bot.send_message(call.message.chat.id, strms, parse_mode='html')

            # file = open(r'1.txt', 'rb')
            # bot.send_document(call.message.chat.id, file)


if __name__ == '__main__':
    bot.infinity_polling()

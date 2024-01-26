import telebot
from telebot import types, custom_filters
from telebot.handler_backends import State, StatesGroup #States
from telebot.storage import StateMemoryStorage
from environs import Env


env = Env()
env.read_env()
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(env('TELEGRAM_BOT_TOKEN'), state_storage=state_storage)


class BotStates(StatesGroup):
    start = State()
    user_has_selected = State()
    approve_pd = State()
    get_phone = State()
    select_service = State()
    select_master = State()
    select_salon = State()
    get_phone = State()
    

# Клавиатура для первого состояния
start_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
start_markup.add(types.KeyboardButton("Позвонить в салон"))
start_markup.add(types.KeyboardButton("Выбрать салон"))
start_markup.add(types.KeyboardButton("Выбрать услугу"))
start_markup.add(types.KeyboardButton("Выбрать мастера"))

# Клавиатура для подтверждения согласия на обработку данных
confirm_agreement_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
confirm_agreement_markup.add(types.KeyboardButton("Принимаю"))
confirm_agreement_markup.add(types.KeyboardButton("Не принимаю"))


salon_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
salon_markup.add(types.KeyboardButton("1 салон"))
salon_markup.add(types.KeyboardButton("2 салон"))


master_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
master_markup.add(types.KeyboardButton("1 мастер"))
master_markup.add(types.KeyboardButton("2 мастер"))


service_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
service_markup.add(types.KeyboardButton("1 услуга"))
service_markup.add(types.KeyboardButton("2 услуга"))

@bot.message_handler(commands=['start'])
def start(message):
    bot.set_state(message.from_user.id, BotStates.user_has_selected, message.chat.id)
    bot.send_message(message.chat.id, "Привет, я бот салона красоты, что бы вы хотели сделать?", reply_markup=start_markup)



@bot.message_handler(state=BotStates.user_has_selected)
def process_start(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['select'] = message.text
    if message.text == "Позвонить в салон":
        bot.send_message(message.chat.id, "Телефон менеджера: +7-921-123-45-67 \n Для записи через бота введите /start")
    else:
        bot.set_state(message.from_user.id, BotStates.approve_pd, message.chat.id)
        bot.send_message(message.chat.id, "Для получения услуг необходимо принять согласие на обработку персональных данных.")
        bot.send_document(message.chat.id, open('agreement.pdf', 'rb'))
        bot.send_message(message.chat.id, "Принимаете согласие?", reply_markup=confirm_agreement_markup)


@bot.message_handler(state=BotStates.approve_pd)
def process_confirm_agreement(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == "Принимаю":
            bot.send_message(message.chat.id, "Согласие принято!", reply_markup=start_markup)
            print(data)
            if data['select'] == 'Выбрать салон':
                bot.set_state(message.from_user.id, BotStates.select_salon, message.chat.id)
                bot.send_message(message.chat.id, "Выберите салон", reply_markup=salon_markup)
            elif data['select'] == 'Выбрать мастера':
                bot.set_state(message.from_user.id, BotStates.select_master, message.chat.id)
                bot.send_message(message.chat.id, "Выберите мастера", reply_markup=master_markup)
            elif data['select'] == 'Выбрать услугу':
                bot.set_state(message.from_user.id, BotStates.select_service, message.chat.id)
                bot.send_message(message.chat.id, "Выберите услугу", reply_markup=service_markup)

        else:
            bot.send_message(message.chat.id, "Вы отказались от согласия. Возвращаемся в начало.", reply_markup=start_markup)
            bot.register_next_step_handler(message, process_start)


@bot.message_handler(state=BotStates.select_salon)
def process_selecting_salon(message):
    bot.send_message(message.chat.id, "Выбираем салон")


@bot.message_handler(state=BotStates.select_master)
def process_selecting_master(message):
    bot.send_message(message.chat.id, "Выбираем мастера")


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)
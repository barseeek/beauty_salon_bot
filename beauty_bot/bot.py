import telebot
from telebot import types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from environs import Env
from django.core.wsgi import get_wsgi_application


env = Env()
env.read_env()
application = get_wsgi_application()
from main.models import Salon, Master, Schedule, Appointment, Service


START_KEYBOARD_BUTTONS = [
    "Позвонить в салон",
    "Выбрать салон",
    "Выбрать услугу",
    "Выбрать мастера"
]
APPROVE_KEYBOARD_BUTTONS = [
    "Принимаю",
    "Не принимаю",
]


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


def get_reply_keyboard(model_objects):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for obj in model_objects:
        button_text = str(obj)
        keyboard.add(types.KeyboardButton(button_text))
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    bot.set_state(message.from_user.id, BotStates.user_has_selected, message.chat.id)
    bot.send_message(message.chat.id,
                     "Привет, я бот салона красоты, что бы вы хотели сделать?",
                     reply_markup=get_reply_keyboard(START_KEYBOARD_BUTTONS))


@bot.message_handler(state=BotStates.user_has_selected)
def process_start(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['select'] = message.text
    delete_keyboard = telebot.types.ReplyKeyboardRemove()
    if message.text == "Позвонить в салон":
        bot.send_message(message.chat.id,
                         "Телефон менеджера: +7-921-123-45-67 \n Для записи через бота введите /start",
                        reply_markup=delete_keyboard)
    else:
        bot.set_state(message.from_user.id, BotStates.approve_pd, message.chat.id)
        bot.send_message(message.chat.id,
                        "Для получения услуг необходимо принять согласие на обработку персональных данных.",
                         reply_markup=delete_keyboard)
        bot.send_document(message.chat.id, open('agreement.pdf', 'rb'))
        bot.send_message(message.chat.id,
                         "Принимаете согласие?",
                         reply_markup=get_reply_keyboard(APPROVE_KEYBOARD_BUTTONS))


@bot.message_handler(state=BotStates.approve_pd)
def process_confirm_agreement(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['approved'] = True if message.text == "Принимаю" else False
        delete_keyboard = telebot.types.ReplyKeyboardRemove()
        if message.text == "Принимаю":
            bot.send_message(message.chat.id,
                             "Согласие принято!",
                             reply_markup=delete_keyboard)
            if data['select'] == 'Выбрать салон':
                salons = list(Salon.objects.values_list('name', flat=True))
                bot.set_state(message.from_user.id,
                              BotStates.select_salon,
                              message.chat.id)
                bot.send_message(message.chat.id,
                                 "Выберите салон",
                                 reply_markup=get_reply_keyboard(salons))
            elif data['select'] == 'Выбрать мастера':
                masters = list(Master.objects.values_list('fullname', flat=True))
                bot.set_state(message.from_user.id,
                              BotStates.select_master,
                              message.chat.id)
                bot.send_message(message.chat.id,
                                 "Выберите мастера",
                                 reply_markup=get_reply_keyboard(masters))
            elif data['select'] == 'Выбрать услугу':
                services = list(Service.objects.values_list('name', flat=True))
                bot.set_state(message.from_user.id,
                              BotStates.select_service,
                              message.chat.id)
                bot.send_message(message.chat.id,
                                 "Выберите услугу",
                                 reply_markup=get_reply_keyboard(services))
        else:
            bot.send_message(message.chat.id,
                             "Вы отказались от согласия. Для записи через бота введите /start",
                             reply_markup=delete_keyboard)
            bot.set_state(message.from_user.id,
                          BotStates.start, message.chat.id)


@bot.message_handler(state=BotStates.select_salon)
def process_selecting_salon(message):
    bot.send_message(message.chat.id, "Выбираем салон")


@bot.message_handler(state=BotStates.select_master)
def process_selecting_master(message):
    bot.send_message(message.chat.id, "Выбираем мастера")


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)
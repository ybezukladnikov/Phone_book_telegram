from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import logger
from math import gcd


first_question, want_play, exit_play, choose_num_can, choose_max_num,start_play,\
    create_name, step_first_pl, input_name, input_surname = range(10)
temp_list = []
list_name = []

def start(update, _):
    logger.my_log(update, _, 'Зашел в программу')
    reply_keyboard = [['Записать контакт', 'Найти контакт', 'Показать все контакты'],['Экспорт контактов', 'Импорт контактов','Выход из программы']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f'Приветствую тебя уважаемый пользователь, {update.effective_user.first_name}!\n'
        'В нашей записной книжке ты можешь:\n'
        '1) Записать контакт.\n'
        '2) Найти контакт.\n'
        '3) Увидеть все контакты.\n'
        '4) Осуществить экспорт всех контактов.\n'
        '5) Осуществить импорт всех контактов.\n'      
        'P.S. Ты можешь завершить программу на любом этапе просто, нужно просто ввести команду:\n'
        '/cancel',
        reply_markup=markup_key,)

    return first_question

def answer_fq(update, _):
    if update.message.text == 'Выход из программы':
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Очень жаль, приходи в следующий раз!'
            'И скажи мне хотя бы Пока)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return exit_play

    elif update.message.text == 'Записать контакт':
        logger.my_log(update, CallbackContext, 'Запись контакта.')

        update.message.reply_text(
            f'{update.effective_user.first_name}\n'
            'Отлично. Начнем c фамилии контакта.\n'
            'Введите его.',reply_markup=ReplyKeyboardRemove()
)
        return input_surname

    # elif update.message.text == 'Играть':
    #     logger.my_log(update, CallbackContext, 'Захотел поиграть.')
    #     reply_keyboard = [['Бот', 'Человек']]
    #     # Создаем простую клавиатуру для ответа
    #     markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    #
    #
    #     update.message.reply_text(
    #         f'{update.effective_user.first_name}\n'
    #         'Выбери с кем ты будешь играть! '
    #         ,
    #         reply_markup=markup_key,)
    #     return want_play
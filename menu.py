from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import logger
from math import gcd
import CRUD
import export_import as ei


first_question, input_num_contact, exit_play, choose_contact, answer_in_search,search,\
    input_description, input_phone, input_name, input_surname = range(10)
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
    elif update.message.text == 'Показать все контакты':
        logger.my_log(update, CallbackContext, 'Показать все контакты.')
        return CRUD.show_all_contact(update, _)

    elif update.message.text == 'Экспорт контактов':
        logger.my_log(update, CallbackContext, 'Экспорт контактов.')
        return ei.export(update, _)

    elif update.message.text == 'Импорт контактов':
        logger.my_log(update, CallbackContext, 'Импорт контактов.')
        return ei.import_csv(update, _)

    elif update.message.text == 'Найти контакт':
        logger.my_log(update, CallbackContext, 'Найти контакт.')
        update.message.reply_text(
            f'{update.effective_user.first_name}\n'
            'Начните вводить либо фамилию либо телефон.\n'
        , reply_markup=ReplyKeyboardRemove()
        )
        return search

def answer_search(update, _):
    logger.my_log(update, _, 'изменить критерии поиска')
    reply_keyboard = [['Изменить критерии поиска'], ['Выйти в основное меню'],['Выйти из программы']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f'{update.effective_user.first_name}!\n'
        'Что будете делать дальше?'
,
        reply_markup=markup_key)

    return answer_in_search

def answer_searchq(update, _):
    if update.message.text == 'Выйти из программы':
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Очень жаль, приходи в следующий раз!'
            'И скажи мне хотя бы Пока)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return exit_play

    if update.message.text == 'Выйти в основное меню':
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Переводим в основное меню',
            reply_markup=ReplyKeyboardRemove(),
        )
        return start(update, _)

    if update.message.text == 'Изменить критерии поиска':
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Повторите ввод.',
            reply_markup=ReplyKeyboardRemove(),
        )
        return search

def answer_choose_contact(update, _):
    print(update.message.text)
    if update.message.text == 'Выйти в основное меню':
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Переводим в основное меню',
            reply_markup=ReplyKeyboardRemove(),
        )
        return start(update, _)

    if update.message.text == 'Выбрать контакт':
        update.message.reply_text(
            'Введите цифру контакта:',
            reply_markup=ReplyKeyboardRemove(),
        )
        return input_num_contact












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
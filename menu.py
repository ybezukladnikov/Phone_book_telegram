from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import logger
import CRUD
import export_import as ei


first_question, input_num_contact, exit_play, choose_contact, answer_in_search,search,\
    input_description, input_phone, input_name, input_surname, action_contact, \
question_change_con, input_surname_ch, input_name_ch, input_tel_ch, input_description_ch = range(16)



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
            'Начните вводить фамилию, имя или телефон.\n'
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

    if update.message.text == 'Выйти в основное меню':
        CRUD.search_res = []
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

def choose_action_contact(update, _):
    if update.message.text == 'Выйти в основное меню':
        CRUD.search_res = []
        logger.my_log(update, CallbackContext, 'Не захотел ничего делать.')
        update.message.reply_text(
            'Переводим в основное меню',
            reply_markup=ReplyKeyboardRemove(),
        )
        return start(update, _)

    if update.message.text == 'Удалить':
        CRUD.delet_contact(update, _)
        update.message.reply_text('Контакт успешно удален. Переводим вас в основное меню.')
        return start(update, _)

    if update.message.text == 'Изменить':
        reply_keyboard = [['Фамилию'], ['Имя'], ['Телефон'], ['Описание']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'{update.effective_user.first_name}!\n'
            'Что будете менять?'
            ,
            reply_markup=markup_key)
        return question_change_con

def choose_what_change_contact(update, _):
    if update.message.text == 'Фамилию':
        update.message.reply_text(
            'Введите новую фамаилию',
            reply_markup=ReplyKeyboardRemove(),
        )
        return input_surname_ch

    if update.message.text == 'Имя':
        update.message.reply_text(
            'Введите новое имя',
            reply_markup=ReplyKeyboardRemove(),
        )
        return input_name_ch

    if update.message.text == 'Телефон':
        update.message.reply_text(
            'Введите новое новый телефон',
            reply_markup=ReplyKeyboardRemove(),
        )
        return input_tel_ch

    if update.message.text == 'Описание':
        update.message.reply_text(
            'Введите новое описание к контакту',
            reply_markup=ReplyKeyboardRemove(),
        )
        return input_description_ch


















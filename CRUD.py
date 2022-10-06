import json
import logging
# import module_candies as bt
# import rational as rt
import menu
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
import check

first_question, input_num_contact, exit_play, choose_contact, answer_in_search,search,\
    input_description, input_phone, input_name, input_surname = range(10)
dict_ph = {}
search_res = []

def surname(update, _):
    global dict_ph
    if check.check_text(update, update.message.text):
        dict_ph['surname'] = (update.message.text).title()
        update.message.reply_text('Отлично. Теперь введите имя контакта.')
        return input_name
    else:
        return input_surname

def name(update, _):
    global dict_ph
    if check.check_text(update, update.message.text):
        dict_ph['name'] = (update.message.text).title()
        update.message.reply_text('Отлично. Теперь введите номер контакта.')
        return input_phone
    else:
        return input_name

def phone(update, _):
    global dict_ph
    if check.check_phone(update, update.message.text):
        dict_ph['tel'] = (update.message.text).title()
        update.message.reply_text('Отлично. Теперь Описание контакта.')
        return input_description
    else:
        return input_phone

def description(update, _):
    global dict_ph
    if check.check_text(update, update.message.text):
        dict_ph['comment'] = (update.message.text).title()
        read_and_write(dict_ph,'rw')
        update.message.reply_text('Отлично. Ваш контакт успешно записан. Переводим вас в основное меню.')

        return menu.start(update, _)
    else:
        return input_description

def read_and_write(dict_ph, arg):
    if arg == 'rw':
        try:
            with open('data_base.json', 'r') as f:
                phone_dir = json.load(f)
        except:
            phone_dir = []

        phone_dir.append(dict_ph)
        with open('data_base.json', 'w') as file:
            json.dump(phone_dir, file, indent=2,ensure_ascii=False)

    elif arg == 'r':
        try:
            with open('data_base.json', 'r') as f:
                phone_dir = json.load(f)
        except:
            phone_dir = []
        return phone_dir

def show_all_contact(update, _):
    phone_dir = read_and_write(dict_ph, 'r')
    if len(phone_dir)==0:
        update.message.reply_text('У вас пока нет контактов. ')
        return menu.start(update, _)
    update.message.reply_text('Найдены следующие контакты: ')
    for num, i in enumerate(phone_dir):
        update.message.reply_text(f'Контакт № {num + 1}: ')
        update.message.reply_text(f'Фамилия: {i["surname"]}\n'
              f'Имя: {i["name"]}\n'
              f'Телефон: {i["tel"]}\n'
              f'Статус: {i["comment"]}\n')

    update.message.reply_text('Переводим вас в основное меню.')
    return menu.start(update, _)

def search_ph(update, _):
    phone_dir = read_and_write(dict_ph, 'r')
    global search_res
    if not (update.message.text).isnumeric():
        for i in phone_dir:
            if update.message.text in i['surname']:
                search_res.append(i)
        if len(search_res) == 0:
            update.message.reply_text('К сожалению, нет совпадений')
            return menu.answer_search(update, _)
        update.message.reply_text(f'Найдено {len(search_res)} контактов: ')
        for num, i in enumerate(search_res):
            update.message.reply_text(f'Контакт № {num + 1}: ')
            update.message.reply_text(f'Фамилия: {i["surname"]}\n'
                                      f'Имя: {i["name"]}\n'
                                      f'Телефон: {i["tel"]}\n'
                                      f'Статус: {i["comment"]}\n')
        reply_keyboard = [['Выбрать контакт'], ['Выйти в основное меню']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'{update.effective_user.first_name}!\n'
            'Что будете делать дальше?'
            ,
            reply_markup=markup_key)

        return choose_contact

def num_contact(update, _):
    global search_res
    if check.check_choose_contact(update, update.message.text):
        print(update.message.text)
    #     dict_ph['tel'] = (update.message.text).title()
    #     update.message.reply_text('Отлично. Теперь Описание контакта.')
    #     return input_description
    # else:
    #     return input_num_contact










    # global dict_ph
    # if check.check_text(update.message.text):
    #     dict_ph['surname'] = (update.message.text).title()
    #     update.message.reply_text('Отлично. Теперь введите имя контакта.')
    #     return input_name
    # else:
    #     update.message.reply_text('Фамилия слишком длинное. Должно быть не менее 20 символов')
    #     return input_surname
















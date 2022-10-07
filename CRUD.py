import json
import logger
import menu
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
import check

first_question, input_num_contact, exit_play, choose_contact, answer_in_search,search,\
    input_description, input_phone, input_name, input_surname, action_contact, \
question_change_con, input_surname_ch, input_name_ch, input_tel_ch, input_description_ch = range(16)

dict_ph = {}
search_res = []
num_con = 0

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

def read_and_wr_ch(text,arg):
    global num_con
    global search_res
    with open('data_base.json', 'r') as f:
        phone_dir = json.load(f)
    temp_num = phone_dir.index(search_res[num_con - 1])
    phone_dir[temp_num][arg] = text
    with open('data_base.json', 'w') as file:
        json.dump(phone_dir, file, indent=2, ensure_ascii=False)



def show_all_contact(update, _):
    logger.my_log(update, _, 'Показал все контакты')
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
    logger.my_log(update, _, 'Поиск контактов')
    phone_dir = read_and_write(dict_ph, 'r')
    global search_res
    if not (update.message.text).isnumeric():
        for i in phone_dir:
            if update.message.text in i['surname'] or update.message.text in i['name'] :
                search_res.append(i)
    else:
        for i in phone_dir:
            if update.message.text in i['tel']:
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
    global num_con
    if check.check_choose_contact(update, update.message.text):
        num_con = int(update.message.text)
        if num_con<1 or num_con>len(search_res):
            update.message.reply_text('Число не соответствует количеству контактов.')
            return input_num_contact

        update.message.reply_text('Вот контакт, который вы выбрали: ')
        update.message.reply_text(f'Контакт № {num_con}: ')
        update.message.reply_text(f'Фамилия: {search_res[num_con-1]["surname"]}\n'
                                  f'Имя: {search_res[num_con-1]["name"]}\n'
                                  f'Телефон: {search_res[num_con-1]["tel"]}\n'
                                  f'Статус: {search_res[num_con-1]["comment"]}\n')
        reply_keyboard = [['Удалить'], ['Изменить'], ['Выйти в основное меню']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'{update.effective_user.first_name}!\n'
            'Что хотитет сделать с контактом?'
            ,
            reply_markup=markup_key)

        return action_contact


    else:
        return input_num_contact

def delet_contact(update, _):
    global num_con
    global search_res
    logger.my_log(update, _, f'Удалил контакт {search_res[num_con - 1]}')
    phone_dir = read_and_write(dict_ph, 'r')
    phone_dir.remove(search_res[num_con-1])
    search_res = []
    with open('data_base.json', 'w') as file:
        json.dump(phone_dir, file, indent=2, ensure_ascii=False)

def choose_change_surname_contact(update, _):
    global num_con
    global search_res
    if check.check_text(update, update.message.text):
        read_and_wr_ch(update.message.text,'surname')
        search_res = []
        update.message.reply_text('Ваш контакт изменен. Переводим вас в начало меню.')
        return menu.start(update, _)
    else:
        return input_surname_ch

def choose_change_name_contact(update, _):
    global num_con
    global search_res
    if check.check_text(update, update.message.text):
        read_and_wr_ch(update.message.text, 'name')
        search_res = []
        update.message.reply_text('Ваш контакт изменен. Переводим вас в начало меню.')
        return menu.start(update, _)
    else:
        return input_name_ch

def choose_change_tel_contact(update, _):
    global num_con
    global search_res
    if check.check_phone(update, update.message.text):
        read_and_wr_ch(update.message.text, 'tel')
        search_res = []
        update.message.reply_text('Ваш контакт изменен. Переводим вас в начало меню.')
        return menu.start(update, _)
    else:
        return input_tel_ch

def choose_change_description_contact(update, _):
    global num_con
    global search_res
    if check.check_text(update, update.message.text):
        read_and_wr_ch(update.message.text, 'comment')
        search_res = []
        update.message.reply_text('Ваш контакт изменен. Переводим вас в начало меню.')
        return menu.start(update, _)
    else:
        return input_description_ch






































import json
import logging
# import module_candies as bt
# import rational as rt
import menu
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
import check

first_question, want_play, exit_play, choose_num_can, choose_max_num,start_play,\
    create_name, step_first_pl, input_name, input_surname = range(10)
dict_ph = {}

def surname(update, _):
    global dict_ph
    if check.check_text(update.message.text):
        dict_ph['surname'] = (update.message.text).title()
        update.message.reply_text('Отлично. Теперь введите имя контакта.')
        return input_name
    else:
        update.message.reply_text('Фамилия слишком длинное. Должно быть не менее 20 символов')
        return input_surname

def name(update, _):
    print(dict_ph)
    # global dict_ph
    # if check.check_text(update.message.text):
    #     dict_ph['surname'] = (update.message.text).title()
    #     update.message.reply_text('Отлично. Теперь введите имя контакта.')
    #     return input_name
    # else:
    #     update.message.reply_text('Фамилия слишком длинное. Должно быть не менее 20 символов')
    #     return input_surname
















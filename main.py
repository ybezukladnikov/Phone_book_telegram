import logging
import CRUD
# import module_candies as bt
# import rational as rt
import menu
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN

def cancel(update, _):
    update.message.reply_text(
        'Если что-то будет нужно, заходи.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, menu.start)],

        states={
            menu.first_question: [MessageHandler(Filters.regex('^(Записать контакт|Найти контакт|'
                                                               'Показать все контакты|'
                                                               'Экспорт контактов|Импорт контактов|'
                                                               'Выход из программы)$'), menu.answer_fq)],

            menu.input_surname:[MessageHandler(Filters.text, CRUD.surname)],
            menu.input_name:[MessageHandler(Filters.text, CRUD.name)],
            menu.input_phone:[MessageHandler(Filters.text, CRUD.phone)],
            menu.input_description:[MessageHandler(Filters.text, CRUD.description)],
            menu.search:[MessageHandler(Filters.text, CRUD.search_ph)],
            menu.answer_in_search:[MessageHandler(Filters.regex('^(Изменить критерии поиска|Выйти в основное меню|'
                                                               'Выйти из программы)'), menu.answer_searchq)],
            menu.choose_contact:[MessageHandler(Filters.regex('^(Выбрать контакт|'
                                                               'Выйти в основное меню)'), menu.answer_choose_contact)],
            menu.input_num_contact:[MessageHandler(Filters.text, CRUD.num_contact)],
            menu.action_contact:[MessageHandler(Filters.regex('^(Удалить|Изменить|Выйти в основное меню)'), menu.choose_action_contact)],
            menu.question_change_con:[MessageHandler(Filters.regex('^(Фамилию|Имя|Телефон|Описание)'), menu.choose_what_change_contact)],
            menu.input_surname_ch:[MessageHandler(Filters.text, CRUD.choose_change_surname_contact)],
            menu.input_name_ch:[MessageHandler(Filters.text, CRUD.choose_change_name_contact)],
            menu.input_description_ch:[MessageHandler(Filters.text, CRUD.choose_change_description_contact)],















            #
            # bt.want_play:[MessageHandler(Filters.regex('^(Бот|Человек)$'), bt.choose_mod)],
            # bt.choose_num_can:[MessageHandler(Filters.text, bt.check_num_can)],
            # bt.choose_max_num:[MessageHandler(Filters.text, bt.check_max_can)],
            # bt.start_play:[MessageHandler(Filters.text, bt.main_func)],
            # bt.create_name:[MessageHandler(Filters.text, bt.check_name)],
            # bt.step_first_pl:[MessageHandler(Filters.text, bt.main_step_first)],
            # bt.step_second_pl:[MessageHandler(Filters.text, bt.main_step_second)],
            #
            #
            menu.exit_play: [MessageHandler(Filters.text, cancel)]
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )





dispatcher.add_handler(conv_handler)



print('server started')
updater.start_polling()
updater.idle()

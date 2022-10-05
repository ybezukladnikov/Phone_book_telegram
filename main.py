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
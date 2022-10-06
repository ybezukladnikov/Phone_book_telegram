def check_text(update, text):
    if len(text)>20:
        update.message.reply_text('Введеное значение слишком длинное. Должно быть не более 20 символов')
        return False
    else:
        return True

def check_phone(update, text):
    if len(text)>12:
        update.message.reply_text('Введеное значение слишком длинное. Должно быть не более 12 символов')
        return False

    for i in text:
        if i.isalpha():
            update.message.reply_text('Введеное значение содержит буквы. Попробуйте снова.')
            return False
    return True

def check_choose_contact(update, text):
    try:
        num = int(text)
        return True
    except:
        update.message.reply_text('Некорректное число попробуйте снова')
        return False






    # if len(text)>12:
    #     update.message.reply_text('Введеное значение слишком длинное. Должно быть не более 12 символов')
    #     return False
    #
    # for i in text:
    #     if i.isalpha():
    #         update.message.reply_text('Введеное значение содержит буквы. Попробуйте снова.')
    #         return False
    # return True




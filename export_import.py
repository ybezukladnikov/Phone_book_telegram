import json
import csv
import CRUD
import menu

dict_ph = {}
def export(update, _):
    phone_dir = CRUD.read_and_write(dict_ph, 'r')
    if len(phone_dir)==0:
        update.message.reply_text('У вас пока нет контактов для экспорта. ')
        return menu.start(update, _)
    count = 0
    with open("phone_directory_export.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["Фамилия\t", "Имя\t", "Телефон\t", "Описание\t"])
        for i in phone_dir:
            file_writer.writerow([i['surname'],i['name'], i['tel'], i['comment']])
            count+=1
    update.message.reply_text(f'Экспорт завершен успешно. Всего экспортировано {count} контактов.\n'
                              f'Переводим вас в основное меню')
    return menu.start(update, _)

def import_csv(update, _):
    result = []
    with open("file_for_import.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter = ",")
        try:
            count = 0
            for row in file_reader:
                if count == 0:
                    count += 1
                    continue

                else:
                    temp_dict = {}
                    temp_dict['surname'] = row[0]
                    temp_dict['name'] = row[1]
                    temp_dict['tel'] = row[2]
                    temp_dict['comment'] = row[3]
                    result.append(temp_dict)
                count += 1
        except:
            update.message.reply_text('Извините, но Файл для импорта не соответствует стандарту. ')
            return menu.start(update, _)
    if len(result)==0:
        update.message.reply_text('Файл для импорта пустой. ')
        return menu.start(update, _)
    count -= 1
    with open('data_base.json', 'w') as file:
        json.dump(result, file, indent=2,ensure_ascii=False)

    update.message.reply_text(f'Импорт завершен успешно. Всего импортировано {count} контактов.\n'
                              f'Переводим вас в основное меню')
    return menu.start(update, _)

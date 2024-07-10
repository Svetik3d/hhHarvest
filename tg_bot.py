import telebot
import data_models
from database import db_scripts
import my_parser
import texts


botTimeWeb = telebot.TeleBot('токен')
active_requests_search = []


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    db_scripts.init_t()
    first_mess = texts.start_text
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html')


@botTimeWeb.message_handler(commands=['search'])
def search(message):
    active_requests_search.append(message.chat.id)
    botTimeWeb.send_message(message.chat.id, texts.search_text, parse_mode='html')


@botTimeWeb.message_handler(func=lambda message: message.chat.id in active_requests_search)
def give_data_search(message):
    try:
        t = message.text.strip().split("\n")

        text = t[0].strip().lower()
        if text == "" or (not text.isalpha()):
            botTimeWeb.send_message(message.chat.id, texts.err_text,
                                    parse_mode='html')
            return

        area = t[1].strip().lower()
        if area == "-":
            area = ""
        else:
            if (area == "1" or area == "москва"):
                area = "1"
            elif (area == "2" or area == "санкт-петербург"):
                area = "2"
            elif (area == "2019" or area == "московская область" or area == "подмосковье"):
                area = "2019"
            else:
                botTimeWeb.send_message(message.chat.id, texts.err_area,
                                    parse_mode='html')
                return

        education = t[2].strip().lower()
        if education == "-":
            education = ""
        else:
            if education == "высшее":
                education = "higher"
            elif education == "среднее профессиональное":
                education = "special_secondary"
            elif (education == "не указано" or education == "не требуется" or education == "не требуется или не указано"):
                education = "not_required_or_not_specified"
            else:
                botTimeWeb.send_message(message.chat.id, texts.err_education,
                                    parse_mode='html')
                return

        salary = t[3].strip()
        if salary == "-":
            salary = ""
        else:
            if not salary.isdigit():
                botTimeWeb.send_message(message.chat.id, texts.err_salary,
                                    parse_mode='html')
                return


        data = data_models.Request(text=text, area=area, education=education,
                                salary=salary, chat_id=message.chat.id)
        botTimeWeb.send_message(message.chat.id, texts.request_accepted,
                                parse_mode='html')
        my_parser.main(data)

        botTimeWeb.send_message(message.chat.id, texts.found_vacancies,
                                parse_mode='html')
        with open("{0}.txt".format(message.chat.id), 'rb') as f:
            botTimeWeb.send_document(message.chat.id, f)

        active_requests_search.remove(message.chat.id)

    except Exception as err:
        print(err)
        botTimeWeb.send_message(message.chat.id, texts.err, parse_mode='html')


@botTimeWeb.message_handler(commands=['show'])
def show(message):
    mess = texts.show_text
    botTimeWeb.send_message(message.chat.id, mess, parse_mode='html')
    db_scripts.get_all_data(message.chat.id)
    with open("{0}.txt".format(message.chat.id), 'rb') as f:
        botTimeWeb.send_document(message.chat.id, f)

botTimeWeb.infinity_polling()

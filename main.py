import telebot
import psycopg2
from datetime import datetime

conn = psycopg2.connect(database="schedule_db1",
                        user="postgres",
                        password="postgres",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

bot = telebot.TeleBot(token)

day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
days_list = ["пн", "вт", "ср", "чт", "пт", "сб"]
week_number = datetime.today().isocalendar()[1] % 2


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row("текущая неделя", "следующая неделя")

    keyboard.row("пн", "вт", "ср", "чт", "пт", "сб")
    bot.send_message(message.chat.id, "Расписание на какой день/неделю вы хотите увидеть?", reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def weekNumber(message):
    if week_number == 1:
        bot.send_message(message.chat.id, "Сейчас идет нечетная неделя")
    else:
        bot.send_message(message.chat.id, "Сейчас идет четная неделя")


@bot.message_handler(commands=['mtuci'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Сайт МТУСИ: https://mtuci.ru/")


@bot.message_handler(commands=['help'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Описание доступных команд:\n"
                                      "/start - активация бота\n"
                                      "/help - информация о доступных командах\n"
                                      "/week - четность/нечетность неделя\n"
                                      "/mtuci - ссылка на официальный сайт МТУСИ\n"
                                      "Нажмите на кнопку нужного дня или недели для вывода расписания")


@bot.message_handler(content_types='text')
def reply(message):
    if 'текущая' in message.text.lower():
        text = ""
        for i in day_list:
            if week_number == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            for j in records:
                if week_number:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = '{i} 1' or day = '{i} 0') and subject = '{j[2]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = '{i} 2' or day = '{i} 0') and subject = '{j[2]}'")

                text += f" Предмет: {j[3]};\n Кабинет: {j[4]};\n Время: {j[5]};\n Преподаватель: {j[6]}\n\n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)

    elif 'следующая' in message.text.lower():
        text = ""
        for i in day_list:
            if week_number + 1 == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            for j in records:
                if week_number + 1 == 1:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = '{i} 1' or day = '{i} 0') and subject = '{j[2]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = '{i} 2' or day = '{i} 0') and subject = '{j[2]}'")

                text += f" Предмет: {j[3]};\n Кабинет: {j[4]};\n Время: {j[5]};\n Преподаватель: {j[6]}\n\n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)

    elif message.text.lower() in days_list:
        if message.text.lower() == "пн":
            if week_number == 1:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Monday 1' or day = 'Monday 0' order by start_time")
            else:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Monday 2' or day = 'Monday 0' order by start_time")
            records = list(cursor.fetchall())
            text = f"{message.text}:\n"
            text += '____________________________________________________________\n'
            for i in records:
                if week_number:
                    cursor.execute(f"SELECT * FROM teacher where (day = 'Monday 1' or day = 'Monday 0') and subject = '{i[3]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = 'Monday 2' or day = 'Monday 0') and subject = '{i[3]}'")
                text += f"Предмет: {i[3]};\n Кабинет: {i[4]};\n Время: {i[5]};\n Преподаватель: {i[6]}\n\n"
            text += "____________________________________________________________"
            bot.send_message(message.chat.id, text)
        elif message.text.lower() == "вт":
            if week_number == 1:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Tuesday 1' or day = 'Tuesday 0' order by start_time")
            else:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Tuesday 2' or day = 'Tuesday 0' order by start_time")
            records = list(cursor.fetchall())
            text = f"{message.text}:\n"
            text += '____________________________________________________________\n'
            for i in records:
                if week_number:
                    cursor.execute(f"SELECT * FROM teacher where (day = 'Tuesday 1' or day = 'Tuesday 0') and subject = '{i[3]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = 'Tuesday 2' or day = 'Tuesday 0') and subject = '{i[3]}'")
                text += f"Предмет: {i[3]};\n Кабинет: {i[4]};\n Время: {i[5]};\n Преподаватель: {i[6]}\n\n"
            text += "____________________________________________________________"
            bot.send_message(message.chat.id, text)
        elif message.text.lower() == "ср":
            if week_number == 1:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Wednesday 1' or day = 'Wednesday 0' order by start_time")
            else:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Wednesday 2' or day = 'Wednesday 0' order by start_time")
            records = list(cursor.fetchall())
            text = f"{message.text}:\n"
            text += '____________________________________________________________\n'
            for i in records:
                if week_number:
                    cursor.execute(f"SELECT * FROM teacher where (day = 'Wednesday 1' or day = 'Wednesday 0') and subject = '{i[3]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = 'Wednesday 2' or day = 'Wednesday 0') and subject = '{i[3]}'")
                text += f"Предмет: {i[3]};\n Кабинет: {i[4]};\n Время: {i[5]};\n Преподаватель: {i[6]}\n\n"
            text += "____________________________________________________________"
            bot.send_message(message.chat.id, text)
        elif message.text.lower() == "чт":
            if week_number == 1:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Thursday 1' or day = 'Thursday 0' order by start_time")
            else:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Thursday 2' or day = 'Thursday 0' order by start_time")
            records = list(cursor.fetchall())
            text = f"{message.text}:\n"
            text += '____________________________________________________________\n'
            for i in records:
                if week_number:
                    cursor.execute(f"SELECT * FROM teacher where (day = 'Thursday 1' or day = 'Thursday 0') and subject = '{i[3]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = 'Thursday 2' or day = 'Thursday 0') and subject = '{i[3]}'")
                text += f"Предмет: {i[3]};\n Кабинет: {i[4]};\n Время: {i[5]};\n Преподаватель: {i[6]}\n\n"
            text += "____________________________________________________________"
            bot.send_message(message.chat.id, text)
        elif message.text.lower() == "пт":
            if week_number == 1:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Friday 1' or day = 'Friday 0' order by start_time")
            else:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Friday 2' or day = 'Friday 0' order by start_time")
            records = list(cursor.fetchall())
            text = f"{message.text}:\n"
            text += '____________________________________________________________\n'
            for i in records:
                if week_number:
                    cursor.execute(f"SELECT * FROM teacher where (day = 'Friday 1' or day = 'Friday 0') and subject = '{i[3]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = 'Friday 2' or day = 'Friday 0') and subject = '{i[3]}'")
                text += f"Предмет: {i[3]};\n Кабинет: {i[4]};\n Время: {i[5]};\n Преподаватель: {i[6]}\n\n"
            text += "____________________________________________________________"
            bot.send_message(message.chat.id, text)
        elif message.text.lower() == "сб":
            if week_number == 1:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Saturday 1' or day = 'Saturday 0' order by start_time")
            else:
                cursor.execute(
                    f"SELECT * FROM timetable where day = 'Saturday 2' or day = 'Saturday 0' order by start_time")
            records = list(cursor.fetchall())
            text = f"{message.text}:\n"
            text += '____________________________________________________________\n'
            for i in records:
                if week_number:
                    cursor.execute(f"SELECT * FROM teacher where (day = 'Saturday 1' or day = 'Saturday 0') and subject = '{i[3]}'")
                else:
                    cursor.execute(
                        f"SELECT * FROM teacher where (day = 'Saturday 2' or day = 'Saturday 0') and subject = '{i[3]}'")
                text += f"Предмет: {i[3]};\n Кабинет: {i[4]};\n Время: {i[5]};\n Преподаватель: {i[6]}\n\n"
            text += "____________________________________________________________"
            bot.send_message(message.chat.id, text)

    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.infinity_polling()

import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import json
import threading

# Замініть цей токен на свій
API_TOKEN = '7903550091:AAGJATUfeILavzIZqoOev8nmfpKlE251siM'
timers = {}
DEFAULT_TIMER = 0
bot = telebot.TeleBot(API_TOKEN)
user_ids_r11 = []
user_ids_f11 = []  # Порожній список для Ф-11
user_ids_p21 = []
Group_id = -1002393266808
homework = {}
notifications_enabled = True
# Приклад розкладу пар і дзвінкі
ads = [
    "\U0001F3A5 VideoVortex – твій ідеальний відеохостинг! Завантажуй, дивись та ділися відео без обмежень!",
    "\U0001F916 Бот 'Цікаві Факти' – дізнавайся щось нове кожного дня! Підпишись та дивуй друзів!",
    "\U0001F6E1\FE0F Бот 'Антиспам' – захисти свій чат від небажаних повідомлень та реклами!",
    "\U0001F4FA VideoVortex підтримує 4K та швидке завантаження! Дивись без лагів!",
    "\U0001F916 'Цікаві Факти' – твій інтелектуальний супутник у світі знань!",
    "\U0001F6E1\FE0F Бот 'Антиспам' – встанови його зараз і забудь про набридливих спамерів!"
]

archived_schedule_r11 = {
    "Понеділок": [
        {"пара": "Математика", "час": "8:40 - 9:40", "посилання": "Посилання на відеозустріч: https://us04web.zoom.us/j/76326629062?pwd=Ser67bbOqxbRDqePySZgEKYktF8Ccv.1"},
        {"пара": "Укр.мова", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч:  https://meet.google.com/dvv-ifnp-oso"},
        {"пара": "Фізика", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч: https://meet.google.com/qzz-cenz-gsj"},
    ],
    "Вівторок": [
        {"пара": "Іноземна мова", "час": "8:40 - 9:40", "посилання": "Посилання на відеозустріч: https://meet.google.com/azp-zzsu-wkf"},
        {"пара": "Всесвітня історія", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/ycf-btbm-kqv"},
        {"пара": "Зарубіжна література", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч: https://meet.google.com/ujy-azik-afz"},
    ],
    "Середа": [
        {"пара": "Географія", "час": "8:40 - 9:40", "посилання": "Посилання на відеозустріч: https://meet.google.com/dns-shjn-zfg"},
        {"пара": "Українська література", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/ouj-urzf-kzr"},
        {"пара": "Інформатика", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч: https://meet.google.com/qsw-avhk-qfn"},
        {"пара": "Фізична культура", "час": "12:30 - 13:30"},
    ],
    "Четвер": [
        {"пара": "Біологія", "час": "8:40 - 9:40", "посилання": "Посилання на відеозустріч: https://meet.google.com/bpn-kdqg-mpa"},
        {"пара": "Астрономія", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/inh-otkm-beo"},
        {"пара": "Математика", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч: https://us04web.zoom.us/j/76326629062?pwd=Ser67bbOqxbRDqePySZgEKYktF8Ccv.1"},
    ],
    "П'ятниця": [
        {"пара": "Хімія", "час": "8:40 - 9:40"},
        {"пара": "Захист України", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/gjc-zkcw-fwk"},
        {"пара": "Зарубіжна література", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч: https://meet.google.com/ujy-azik-afz"},
    ],
}
schedule_r11 = {
    "Понеділок": [
        {"пара": "Географія", "час": "8:40 -9:40", "посилання": "Посилання на відеозустріч: https://meet.google.com/dns-shjn-zfg"},
        {"пара": "Фізика", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/qzz-cenz-gsj"},
        {"пара": "Іноземна мова", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч (2 підгрупа): https://meet.google.com/azp-zzsu-wkf"},
    ],
    "Вівторок": [
        {"пара": "Економічна теорія", "час": "8:40 - 9:40"},
        {"пара": "Математика", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://us04web.zoom.us/j/76326629062?pwd=Ser67bbOqxbRDqePySZgEKYktF8Ccv.1"},
        {"пара": "Українська література", "час": "11:00 - 12:00", "посилання": "Посилання на відеозустріч: https://meet.google.com/ouj-urzf-kzr"},
    ],
    "Середа": [
        {"пара": "Фізична культура", "час": "8:40 - 9:40"},
        {"пара": "Захист України", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/gjc-zkcw-fwk"},
        {"пара": "Інформатика", "час": "11:00 -12:00", "посилання": "Посилання на відеозустріч: https://meet.google.com/qsw-avhk-qfn"},
        {"пара": "Біологія/Людина і світ", "час": "12:30 - 13:30", "посилання": "Посилання на відеозустріч (Біологія): https://meet.google.com/bpn-kdqg-mpa"},
    ],
    "Четвер": [
        {"пара": "Українська мова", "час": "8:40 - 9:40", "посилання": "Посилання на відеозустріч:  https://meet.google.com/dvv-ifnp-oso"},
        {"пара": "Всесвітня історія", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч: https://meet.google.com/ycf-btbm-kqv"},
        {"пара": "Культурологія", "час": "11:00 - 12:00"},
    ],
    "П'ятниця": [
        {"пара": "Біологія", "час": "8:40 - 9:40", "посилання": "Посилання на відеозустріч: https://meet.google.com/bpn-kdqg-mpa"},
        {"пара": "Захист України/Хімія", "час": "9:50 - 10:50", "посилання": "Посилання на відеозустріч (Захист України): https://meet.google.com/gjc-zkcw-fwk"},
        {"пара": "Хімія", "час": "11:00 - 12:00"},
    ],
}
schedule_p21 = {
    "Понеділок": [
        {"пара": "Історія України", "час": "8:40 - 9:40"},
        {"пара": "Математичний аналіз", "час": "9:50 - 10:50"},
        {"пара": "Основи програмування", "час": "11:00 - 12:00"},
    ],
    "Вівторок": [
        {"пара": "Лінійна алгебра та аналітична геометрія", "час": "8:40 - 9:40"},
        {"пара": "Екологія", "час": "9:50 - 10:50"},
        {"пара": "Економічна теорія", "час": "11:00 - 12:00"},
        {"пара": "Правознавство", "час": "12:30 - 13:30"},
    ],
    "Середа": [
        {"пара": "Основи програмування", "час": "8:40 - 9:40"},
        {"пара": "Іноземна мова", "час": "9:50 - 10:50"},
        {"пара": "Історія України (факультатив)", "час": "11:00 - 12:00"},
    ],
    "Четвер": [
        {"пара": "Математичний логіка", "час": "8:40 - 9:40"},
        {"пара": "Математика", "час": "9:50 - 10:50"},
        {"пара": "Фізика", "час": "11:00 - 12:00"},
        {"пара": "Фізична культура", "час": "12:30 - 13:30"},
    ],
    "П'ятниця": [
        {"пара": "Лінійна алгебра та аналітична геометрія", "час": "8:40 - 9:40"},
        {"пара": "Українська мова", "час": "9:50 - 10:50"},
        {"пара": "Українська література", "час": "11:00 - 12:00"},
    ],
}
schedule_f11 = {
    "Понеділок": [
        {"пара": "-", "час": "8:40 - 9:40"},
        {"пара": "Іноземна мова", "час": "9:50 - 10:50"},
        {"пара": "Правознавство", "час": "11:00 - 12:00"},
        {"пара": "Математика", "час": "12:30 - 13:30"},
    ],
    "Вівторок": [
        {"пара": "-/Захист України", "час": "8:40 - 9:40"},
        {"пара": "Географія", "час": "9:50 - 10:50"},
        {"пара": "Біологія", "час": "11:00 - 12:00"},
    ],
    "Середа": [
        {"пара": "-", "час": "8:40 - 9:40"},
        {"пара": "Фізична культура", "час": "9:50 - 10:50"},
        {"пара": "Українська мова", "час": "11:00 - 12:00"},
        {"пара": "Захист України", "час": "12:30 - 13:30"},
    ],
    "Четвер": [
        {"пара": "Хімія", "час": "8:40 - 9:40"},
        {"пара": "Українська література", "час": "9:50 - 10:50"},
        {"пара": "Математика", "час": "11:00 - 12:00"},
        {"пара": "Фізика", "час": "12:30 - 13:30"},
    ],
    "П'ятниця": [
        {"пара": "Біологія/Хімія", "час": "8:40 - 9:40"},
        {"пара": "Фізика", "час": "9:50 - 10:50"},
        {"пара": "Інформатика", "час": "11:00 - 12:00"},
        {"пара": "Всесвітня історія", "час": "12:30 - 13:30"},
    ],
}
archived_schedule_f11 = {
    "Понеділок": [
        {"пара": "Фізична культура", "час": "8:40 - 9:40"},
        {"пара": "Математика", "час": "9:50 - 10:50"},
        {"пара": "Фізика", "час": "11:00 - 12:00"},
    ],
    "Вівторок": [
        {"пара": "-", "час": "8:40 - 9:40"},
        {"пара": "Іноземна мова", "час": "9:50 - 10:50"},
        {"пара": "Інформатика", "час": "11:00 - 12:00"},
        {"пара": "Зарубіжна література", "час": "12:30 - 13:30"},
    ],
    "Середа": [
        {"пара": "Українська література", "час": "8:40 - 9:40"},
        {"пара": "Астрономія", "час": "9:50 - 10:50"},
        {"пара": "Всесвітня історія", "час": "11:00 - 12:00"},
    ],
    "Четвер": [
        {"пара": "Зарубіжна література", "час": "8:40 - 9:40"},
        {"пара": "Біологія", "час": "9:50 - 10:50"},
        {"пара": "Українська мова", "час": "11:00 - 12:00"},
        {"пара": "Фізика", "час": "12:30 - 13:30"},
    ],
    "П'ятниця": [
        {"пара": "Математика", "час": "8:40 - 9:40"},
        {"пара": "Географія", "час": "9:50 - 10:50"},
        {"пара": "Хімія", "час": "11:00 - 12:00"},
    ],
}
bells_schedule = {
    "8:40 - 9:40": "Перша пара",
    "9:50 - 10:50": "Друга пара",
    "11:00 - 12:00": "Третя пара",
     "12:30 - 13:30": "Чеверта пара",
    # Додайте інші дзвінки
}
SCHEDULE_FILE = 'schedules.json'

# Функція для завантаження даних з файлу
def load_schedules():
    try:
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Функція для збереження даних у файл
def save_schedules():
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(personal_schedules, f, ensure_ascii=False, indent=4)

# Завантаження розкладів при запуску бота
personal_schedules = load_schedules()

# Промокод для доступу
promo_code = "FREEACCESS"  # Пример промокоду

# Команда для введення промокоду
@bot.message_handler(commands=['promocode'])
def check_promo(message):
    global promo_code
    if message.text.split()[-1] == promo_code:
        bot.reply_to(message, "Промокод вірний! Ви отримали доступ до розпорядку дня.")
        personal_schedules[message.chat.id] = []  # Створюємо порожній розпорядок для користувача
        save_schedules()  # Зберігаємо зміни
    else:
        bot.reply_to(message, "Невірний промокод. Спробуйте ще раз.")

# Команда для додавання активності до розпорядку дня
# @bot.message_handler(commands=['add_activity'])
# def add_activity(message):
#     if message.chat.id not in personal_schedules:
#         bot.reply_to(message, "Ви ще не ввели промокод для доступу до розпорядку дня. Використайте команду /promocode.")
#     else:
#         bot.reply_to(message, "Введіть активність у форматі: Назва активності, Час (наприклад, 7:00 - 8:00), опис (необов'язково).")

# # Функція для обробки введення активності
# @bot.message_handler(func=lambda message: True)
# def save_activity(message):
#     activity_details = message.text.split(",")
#     if len(activity_details) < 2:
#         bot.reply_to(message, "Невірний формат. Спробуйте ще раз.")
#         return

#     activity = {
#         "активність": activity_details[0].strip(),
#         "час": activity_details[1].strip(),
#         "опис": activity_details[2].strip() if len(activity_details) > 2 else None
#     }

#     personal_schedules[message.chat.id].append(activity)
#     save_schedules()
#     bot.reply_to(message, f"Активність додана: {activity['активність']} з {activity['час']}.")

# # Команда для показу розпорядку дня на поточний день
# @bot.message_handler(commands=['show_schedule'])
# def show_schedule(message):
#     if message.chat.id not in personal_schedules:
#         bot.reply_to(message, "Ви ще не ввели промокод для доступу до розпорядку дня. Використайте команду /promocode.")
#         return

#     current_day = datetime.now().strftime('%A')
#     user_schedule = personal_schedules.get(message.chat.id, [])
#     todays_schedule = [activity for activity in user_schedule if current_day in activity.get('час', '')]

#     if todays_schedule:
#         response = f"Ваш розпорядок на сьогодні ({current_day}):\n"
#         for activity in todays_schedule:
#             response += f"{activity['активність']} - {activity['час']}"
#             if activity['опис']:
#                 response += f" ({activity['опис']})"
#             response += "\n"
#     else:
#         response = f"У вас немає активностей на сьогодні ({current_day})."

#     bot.reply_to(message, response)

# # Команда для видалення активності
# @bot.message_handler(commands=['remove_activity'])
# def remove_activity(message):
#     if message.chat.id not in personal_schedules:
#         bot.reply_to(message, "Ви ще не ввели промокод для доступу до розпорядку дня. Використайте команду /promocode.")
#         return

#     user_schedule = personal_schedules[message.chat.id]
#     if not user_schedule:
#         bot.reply_to(message, "У вас немає активностей для видалення.")
#         return

#     # Виводимо список активностей
#     response = "Виберіть активність для видалення, надіславши її індекс (номер з списку):\n"
#     for i, activity in enumerate(user_schedule, 1):
#         response += f"{i}. {activity['активність']} - {activity['час']}\n"

#     bot.reply_to(message, response)

#     # Очищуємо повідомлення від користувача для вибору активності
#     @bot.message_handler(func=lambda message: message.text.isdigit())
#     def confirm_removal(message):
#         activity_index = int(message.text) - 1
#         if 0 <= activity_index < len(user_schedule):
#             removed_activity = user_schedule.pop(activity_index)
#             save_schedules()
#             bot.reply_to(message, f"Активність '{removed_activity['активність']}' видалена.")
#         else:
#             bot.reply_to(message, "Невірний індекс. Спробуйте ще раз.")
# Команда для донату
@bot.message_handler(commands=['donate'])
def donate(message):
    # Інформація про донат
    donation_message = (
        "Дякуємо за ваш інтерес підтримати нашого бота!\n\n"
        "Ви можете зробити донат за допомогою таких платформ:\n"
        "1. PayPal: https://www.paypal.com/donate?hosted_button_id=XXXXX\n"
        "2. Patreon: https://www.patreon.com/XXXXX\n\n"
        "Ваша підтримка допомагає розвитку бота та додаванню нових функцій! ❤️"
    )
    bot.reply_to(message, donation_message)
def get_start_time(time_range):
    start_time = time_range.split(" - ")[0]
    return datetime.strptime(start_time, "%H:%M").time()

# Список часу, за який потрібно надіслати нагадування
reminder_times = ["8:38", "9:48", "10:58", "12:04", "13:38"]

# Функція для перевірки та надсилання повідомлень за 2 хвилини до початку
def notify_upcoming_lessons():
    while True:
        if notifications_enabled:
            now = datetime.now()
            current_time = now.strftime("%H:%M")  # Тепер порівнюємо час у форматі "HH:MM"
            current_day = now.strftime("%A")

            print(f"Перевірка часу: {current_time}, день тижня: {current_day}")  # Лог для перевірки

            # Перевірка, чи час поточної пари співпадає з часом в списку reminder_times
            if current_time in reminder_times:
                # Перевірка розкладу для кожної групи
                schedules = [
                    (schedule, user_ids_r11, Group_id),  # Для групи Р-11 повідомлення в групу
                    (schedule_f11, user_ids_f11, None),  # Для групи Ф-11 повідомлення приватно
                    (schedule_p21, user_ids_p21, None),  # Для групи П-21 повідомлення приватно
                ]

                for schedule, user_ids, group_id in schedules:
                    if current_day in schedule:
                        for lesson in schedule[current_day]:
                            start_time = get_start_time(lesson["час"]).strftime("%H:%M")

                            # Лог для перевірки часу пари
                            print(f"Перевіряємо: {lesson['пара']} - стартує о {start_time}")

                            # Перевірка, чи поточний час співпадає з початком пари
                            if start_time == current_time:
                                message = f"Незабаром почнеться пара: {lesson['пара']} ({lesson['час']})"
                                print(f"Надсилання повідомлення: {message}")  # Лог для перевірки
                                if user_ids:  # Якщо є ID користувачів для приватних повідомлень
                                    for user_id in user_ids:
                                        bot.send_message(user_id, message)
                                else:
                                    # Якщо немає ID користувачів для приватних повідомлень, надсилаємо в групу
                                    bot.send_message(group_id, message)

                                time.sleep(60)  # Затримка 60 секунд, щоб не надіслати повідомлення кілька разів

        time.sleep(30)  # Перевіряє кожні 30 секунд



# Команда для увімкнення/вимкнення нагадувань
@bot.message_handler(commands=['notifications'])
def toggle_notifications(message):
    global notifications_enabled
    if notifications_enabled:
        notifications_enabled = False
        bot.reply_to(message, "Нагадування вимкнено.")
    else:
        notifications_enabled = True
        bot.reply_to(message, "Нагадування увімкнено.")
def get_random_ad():
    return random.choice(ads)
# Запуск потоку нагадувань
notification_thread = threading.Thread(target=notify_upcoming_lessons)
notification_thread.daemon = True
notification_thread.start()
# Обробка команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я Розкладник. Введи команду /rozklad_r11 для групи Р-11, а для групи Ф-11, то /rozklad_f11, і для групи П-21 (2курс) введи команду /rozklad_p21, щоб отримати розклад пар, а якщо дзвінків, то /dzvinky.")
def create_archive_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Архівний розклад", callback_data="archived_schedule_r11"))
    return markup
def create_archive_f11_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Архівний розклад", callback_data="archived_schedule_f11"))
    return markup
def is_bot_admin(chat_id):
    try:
        chat_admins = bot.get_chat_administrators(chat_id)
        bot_id = bot.get_me().id
        return any(admin.user.id == bot_id for admin in chat_admins)
    except Exception as e:
        print(f"Помилка перевірки адміністратора в чаті {chat_id}: {e}")
        return False

# Команда для встановлення таймера для конкретного чату
@bot.message_handler(commands=['settimer'])
def set_timer(message):
    try:
        _, seconds = message.text.split()
        seconds = int(seconds)

        if seconds < 0:
            bot.send_message(message.chat.id, "Час не може бути від'ємним.")
            return

        timers[message.chat.id] = seconds
        if seconds == 0:
            bot.send_message(message.chat.id, "Таймер вимкнено. Повідомлення більше не будуть видалятися.")
        else:
            bot.send_message(message.chat.id, f"Час таймера встановлено на {seconds} секунд.")
    except ValueError:
        bot.send_message(message.chat.id, "Неправильний формат. Використовуйте: /settimer <час у секундах>")

# Обробка команди /rozklad
@bot.message_handler(commands=['rozklad_r11'])
def send_schedule(message):
    ads = get_random_ad()
    response = "Розклад на тиждень:\n\n"

    # Перебір днів та занять
    for day, classes in schedule_r11.items():
        response += f"*{day}:*\n"
        for lesson in classes:
            link = lesson.get('посилання', '')
            if message.chat.id == Group_id:
                response += f" - {lesson['пара']} ({lesson['час']}) {link if link else '- Посилання немає'}\n"
            else:
                response += f" - {lesson['пара']} ({lesson['час']})\n"
        response += "\n"


    # Відправка повідомлення з розкладом
    chat_id = message.chat.id
    seconds = timers.get(chat_id, DEFAULT_TIMER)
    info_msg = bot.send_message(chat_id, response, parse_mode="Markdown")

    if seconds == 0:
        return
    # Надсилаємо друге повідомлення з лічильником
    countdown_msg = bot.send_message(chat_id, f"Це повідомлення буде вилучено через {seconds} секунд.")

    # Функція для оновлення лічильника і видалення повідомлень
    def countdown_and_delete(chat_id, message, seconds, info_msg, countdown_msg):
        remaining = seconds
        while remaining > 0:
            try:
                # Оновлення кожні 3 секунди (замість 1)
                if remaining % 3 == 0 or remaining <= 5:
                    bot.edit_message_text(f"Це повідомлення буде вилучено через {remaining} секунд.",
                                          chat_id=chat_id, message_id=countdown_msg.message_id)
                time.sleep(1)
                remaining -= 1

            except telebot.apihelper.ApiException as e:
                if "Too Many Requests" in str(e):
                    retry_after = int(str(e).split("retry after ")[1].split()[0])
                    print(f"Отримано помилку 429. Чекаємо {retry_after} секунд перед повторним запитом...")
                    time.sleep(retry_after)
                else:
                    break

        # Після завершення лічильника, видаляємо повідомлення
        try:
            bot.delete_message(chat_id, info_msg.message_id)  # Видаляємо розклад
            bot.delete_message(chat_id, countdown_msg.message_id)  # Видаляємо таймер
            bot.delete_message(chat_id, message.message_id)  # Видаляємо команду користувача
        except telebot.apihelper.ApiException as e:
            print(f"Помилка видалення повідомлення бота в чаті {chat_id}: {e}")



    # Запускаємо оновлення лічильника в окремому потоці
    threading.Thread(target=countdown_and_delete, args=(chat_id, message, seconds, info_msg, countdown_msg)).start()

@bot.callback_query_handler(func=lambda call: call.data == "archived_schedule_r11")
def send_archived_schedule(call):
    response = "Архівний розклад для групи Р-11:\n"
    for day, lessons in archived_schedule_r11.items():
        response += f"\n{day}:\n"
        for lesson in lessons:
            response += f"- {lesson['пара']} ({lesson['час']})\n"

    # Відправка архівного розкладу
    bot.send_message(call.message.chat.id, response)

@bot.message_handler(commands=['zaminy'])
def send_replacements(message):
    ads = get_random_ad()
    bot.reply_to(message, "Оновленні заміни доступні у файлі за посиланням нижче. https://docs.google.com/spreadsheets/d/1WfqBmM996nKjzw6655q1ulLFlqXXR61m/edit?usp=drivesdk&ouid=107056034465924364952&rtpof=true&sd=true", parse_mode="Markdown")
@bot.message_handler(commands=['rozklad_p21'])
def send_schedule_p21(message):
    response = "Розклад на тиждень:\n\n"
    for day, classes in schedule_p21.items():
        response += f"*{day}:*\n"
        for lesson in classes:
                response += f"  - {lesson['пара']} ({lesson['час']})\n"
        response += "\n"
    bot.reply_to(message, response, parse_mode="Markdown")
@bot.message_handler(commands=['rozklad_f11'])
def send_schedule_f11(message):
    response = "Розклад на тиждень:\n\n"
    for day, classes in schedule_f11.items():
        response += f"*{day}:*\n"
        for lesson in classes:
                response += f"  - {lesson['пара']} ({lesson['час']})\n"
        response += "\n"

    chat_id = message.chat.id
    seconds = timers.get(chat_id, DEFAULT_TIMER)
    info_msg_f11 = bot.send_message(chat_id, response, parse_mode="Markdown")

    if seconds == 0:
        return

    # Надсилаємо друге повідомлення з лічильником
    countdown_msg_f11 = bot.send_message(chat_id, f"Це повідомлення буде вилучено через {seconds} секунд.")

    # Функція для оновлення лічильника і видалення повідомлень
    def countdown_and_delete(chat_id, message, seconds, info_msg_f11, countdown_msg_f11):
        remaining = seconds
        while remaining > 0:
            try:
                # Оновлення кожні 3 секунди (замість 1)
                if remaining % 3 == 0 or remaining <= 5:
                    bot.edit_message_text(f"Це повідомлення буде вилучено через {remaining} секунд.",
                                          chat_id=chat_id, message_id=countdown_msg_f11.message_id)
                time.sleep(1)
                remaining -= 1

            except telebot.apihelper.ApiException as e:
                if "Too Many Requests" in str(e):
                    retry_after = int(str(e).split("retry after ")[1].split()[0])
                    print(f"Отримано помилку 429. Чекаємо {retry_after} секунд перед повторним запитом...")
                    time.sleep(retry_after)
                else:
                    break

        # Після завершення лічильника, видаляємо повідомлення
        try:
            bot.delete_message(chat_id, info_msg_f11.message_id)  # Видаляємо розклад
            bot.delete_message(chat_id, countdown_msg_f11.message_id)  # Видаляємо таймер
        except telebot.apihelper.ApiException as e:
            print(f"Помилка видалення повідомлення бота в чаті {chat_id}: {e}")

        # Видалення команди користувача (якщо бот адміністратор)
        if is_bot_admin(chat_id):
            try:
                bot.delete_message(chat_id, message.message_id)  # Видаляємо команду користувача
            except telebot.apihelper.ApiException as e:
                print(f"Не вдалося видалити команду користувача в чаті {chat_id}: {e}")
        else:
            command = message.text.split(' ')[0]
            bot.send_message(chat_id, f"Повідомлення {command} не було вилучено, оскільки я не маю прав адміністратора. Додайте мене як адміністратора, щоб міг вилучати повідомлення з командою.")
            print(f"⚠️ Бот не є адміністратором у чаті {chat_id}, тому команда користувача не буде видалена.")

    # Запускаємо оновлення лічильника в окремому потоці
    threading.Thread(target=countdown_and_delete, args=(chat_id, message, seconds, info_msg_f11, countdown_msg_f11)).start()

@bot.callback_query_handler(func=lambda call: call.data == "archived_schedule_f11")
def send_archived_f11_schedule(call):
    response = "Архівний розклад для групи Ф-11:\n"
    for day, lessons in archived_schedule_f11.items():
        response += f"\n{day}:\n"
        for lesson in lessons:
            response += f"- {lesson['пара']} ({lesson['час']})\n"

    # Відправка архівного розкладу
    bot.send_message(call.message.chat.id, response)
# Обробка команди /dzvinky
@bot.message_handler(commands=['dzvinky'])
def send_bells_schedule(message):
    response = "Розклад дзвінків:\n\n"
    for time, period in bells_schedule.items():
        response += f"*{period}:* {time}\n"
    response += "\n"

    response += f"\n{ads}" if ads else ""
    bot.reply_to(message, response, parse_mode="Markdown")
# Обробка команди /addhomework
@bot.message_handler(commands=['addhomework'])
def ask_subject(message):
    # Запитуємо предмет
    msg = bot.reply_to(message, "Введіть предмет:")
    bot.register_next_step_handler(msg, get_homework)

def get_homework(message):
    subject = message.text
    msg = bot.reply_to(message, f"Введіть завдання для предмету {subject}:")
    bot.register_next_step_handler(msg, save_homework, subject)

def save_homework(message, subject):
    hw = message.text
    if subject in homework:
        homework[subject].append(hw)
    else:
        homework[subject] = [hw]

    bot.reply_to(message, f"Домашнє завдання для {subject} додано!")

# Обробка команди /homework
@bot.message_handler(commands=['homework'])
def show_homework(message):
    if homework:
        response = "Домашні завдання:\n\n"
        for subject, tasks in homework.items():
            response += f"*{subject}:*\n"
            for task in tasks:
                response += f"  - {task}\n"
            response += "\n"
        bot.reply_to(message, response, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Домашніх завдань поки немає.")

# Запуск бота
while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=30)
    except Exception as e:
        print(f"⚠️ Помилка: {e}")
        time.sleep(5)

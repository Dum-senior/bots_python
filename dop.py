import logging #сохранение и вывод сообщений  
import telebot # вы можете создать и настроить собственный чат-бот для использования с 
#Telegram и обеспечить бесперебойный канал связи между вашими пользователями и вашим бизнесом или сервисом
import os # работа с файловой системой, управление переменными окружения,
#обработка сложных путей к файлам, вызов внешних команд оболочки, создание и удаление каталогов и многое другое. 

logging.basicConfig(level=logging.INFO) # 'logging.INFO', что означает, что будут записываться сообщения с уровнем серьезности INFO или выше

# Define file name and path (Определите имя файла и путь к нему)
TOKEN_FILE = 'telegram_token.txt' #создание переменной и помещение туда значения 
TOKEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), TOKEN_FILE) # конструирует путь к файлу-тектону. 

# Open file and read token(открыть файл и считать оттуда токен)
with open(TOKEN_PATH, 'r') as file: # открытия файла в режиме чтения для чтения его содержимого
    token = file.read().strip() #

# Create a bot instance (Создайте экземпляр бота)
bot = telebot.TeleBot(token)# читает и сохраняет содержимое файла по указанному пути к файлу в переменной с именем 'token'

# Global variable to store user's name (Глобальная переменная для хранения имени пользователя)
user_name = ''#создает пустую строковую переменную с именем 'user_name'.

# Start command (запуск команды)
@bot.message_handler(commands=['start'])#(после надписи старт запускается функция)
def start_command(message):# запуск поманды для отправки сообщения
    print(message.chat.id)# идентификация чат id пользователя
    bot.send_message(message.chat.id, 'Добро пожаловать в бот компании Elik*s! Чтобы отправить запрос, используйте команду /request.')
#отправляет сообщение в чат()
# Request command
@bot.message_handler(commands=['request'])#(запуск другой функции)
def request_command(message):# запускает команду 
    bot.send_message(message.chat.id, 'Пожалуйста, предоставьте следующую информацию:\n\nКак вас зовут?')#(отправляет сообщение и ждёт ответа)
    bot.register_next_step_handler(message, process_name)# обработки следующего входного сообщения от 
    #пользователя и передачи его функции 'process_name' для дальнейшей обработки.


# Name state(Состояние имени)
def process_name(message):# создание функции для имени 
    global user_name# сохранение имени 
    user_name = message.text# преобразование в текат
    bot.send_photo(message.chat.id, photo=open('2222.jpg', 'rb'))# отправка пользователю фото
    bot.send_message(message.chat.id, 'Пожалуйста напишите проблему, с которой вы столкнулись, или же выберите из предложенных')
    #отправка пользователю вопросительного предлодения

    # Button(кнопки )
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True) # создание клавиатуры
    buttons = ['Ремонт компьютеров', 'Вопросы по видеонаблюдению', 'Ремонт Оргтехники', 'Ксерокопия', 'Ремонт смартфонов', 'Заказать консультацию', 'Нужны комплектующие', 'Продажа расходных материалов']
    for button in buttons:
        keyboard.add(button) # добавили клавиатуру в кнопки

    bot.send_message(message.chat.id, 'Список часто оказываемых услуг:', reply_markup=keyboard) # выпадают кнопки и клава вместк
    bot.register_next_step_handler(message, process_data)#  передачи его функции для дальнейшей обработки

# Data state(статус данных)
def process_data(message):#
    selected_button = message.text# сохранение выбранной кнопки или же написанного сообщения

    # Ask for phone number after button selection(спросит номер после выбора кнопки)
    bot.send_message(message.chat.id, 'Какой у вас номер телефона?')#отправка пользователю сообщения
    bot.register_next_step_handler(message, lambda msg: process_phone(msg, selected_button))# сохранение в переменные 

# Phone state(стутус номера)
def process_phone(message, selected_button):# вызов функции 
    phone = message.text#сохранение номера телефона


    # Send the request as a message to yourself (Отправить запрос в виде сообщения себе)
    message_text = f"Новая заявка:\nИмя: {user_name} \nНомер: {phone}\nУслуга: {selected_button}"# создаёт заявки, выгрузка значений из переменных
    bot.send_message(chat_id='твой id', text=message_text)# бот пишет админу инфу

    # Send confirmation message to the user
    bot.send_message(message.chat.id, 'Благодарим вас за отправку вашего запроса! Мы свяжемся с вами как можно скорее.(если хотите составить новую заявку, нажмите на /start')
#бот шлёт пользователю контрольное сообщение
if __name__ == '__main__':# Если это условие истинно, то выполняется следующий за ним блок кода
    # Start bot polling
    bot.polling()# команда пишет о том, что бот готов к работе

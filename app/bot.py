import telebot
import pymongo

bot = telebot.TeleBot("7167905109:AAGdNE6D4wwPw-wjQ-hV0V5df-mRwEKMCts")

# Підключення до бази даних MongoDB
client = pymongo.MongoClient("mongodb://admin:password@mongo:27017/")
db = client["url_shortener"]
collection = db["links"]


# Обробка команди start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to URL shortener bot! Send me a link and I'll shorten it for you.")


# Обробка текстових повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Якщо текст - це посилання
    if message.text.startswith("http"):
        doc = {"original_url": message.text}
        result = collection.insert_one(doc)
        short_id = str(result.inserted_id)
        bot.send_message(message.chat.id, f"Shortened link ID: {short_id}")
    # Якщо текст - це коротке посилання
    else:
        doc = collection.find_one({"_id": message.text})
        if doc:
            original_url = doc["original_url"]
            bot.send_message(message.chat.id, f"Original URL: {original_url}")
        else:
            bot.send_message(message.chat.id, "Invalid or unknown shortened link.")


# Обробка команди /my_urls
@bot.message_handler(commands=['my_urls'])
def handle_my_urls(message):
    user_links = collection.find({"user_id": message.from_user.id})
    response = "Your shortened URLs:\n"
    for link in user_links:
        response += f"ID: {link['_id']}, Original URL: {link['original_url']}\n"
    bot.send_message(message.chat.id, response)


# Запуск бота
bot.polling()

import telebot
import requests

from app.main import get_user_links

bot = telebot.TeleBot("7167905109:AAGdNE6D4wwPw-wjQ-hV0V5df-mRwEKMCts")


# Функція для відправки коротких посилань через FastAPI додаток
def send_url_to_shortener(original_url):
    link_data = {"original_url": original_url}
    response = requests.post("http://127.0.0.1:8000/shorten/", json=link_data)
    if response.status_code == 200:
        short_link = response.json().get("short_id")
        return short_link
    else:
        return None


# Функція для отримання кількості переходів за коротким посиланням
def get_click_count(short_id):
    response = requests.get(f"http://127.0.0.1:8000/clicks/{short_id}/")
    if response.status_code == 200:
        click_count = response.json().get("click_count")
        return click_count
    else:
        return None


# Обробка текстових повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith("http"):
        # Отримати посилання з повідомлення
        link_url = message.text
        # Відправити посилання на скорочення через FastAPI
        short_link = send_url_to_shortener(link_url)
        if short_link:
            bot.send_message(message.chat.id, f"Shortened link: {short_link}")
        else:
            bot.send_message(message.chat.id, "Error occurred while shortening link")
    else:
        bot.send_message(message.chat.id, "Please provide a valid URL")


# Обробка команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the URL shortener bot! Send me a URL and I'll shorten it for you.")


# Обробка команди /my_urls
@bot.message_handler(commands=['my_urls'])
def send_my_urls(message):
    # Отримайте список посилань користувача з MongoDB
    user_id = message.chat.id
    user_links = get_user_links(user_id)
    if user_links:
        links_message = "Your links:\n" + "\n".join(user_links)
        bot.send_message(message.chat.id, links_message)
    else:
        bot.send_message(message.chat.id, "You haven't added any links yet.")



bot.polling()

# Запуск бота
bot.polling()

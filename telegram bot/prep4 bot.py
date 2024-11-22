import os
import signal
import sys
import telebot
import json
from github import Github
import dotenv
from telegram import Message
# Authentication is defined via github.Auth
from github import Auth



dotenv.load_dotenv()
auth = Auth.Token(os.environ.get('GITHUB_ACCESS_TOKEN'))
# Public Web Github
g = Github(auth=auth)
repo = g.get_user().get_repo(os.environ.get('GITHUB_REPO'))
print(repo.name)
# for repo in g.get_user().get_repos():
#     print(repo.name)


# Telegram bot token
TELEGRAM_TOKEN = '7850073319:AAGZdRj5V7EODwLugS7oeHSf1frRF2EDPI0'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

def pretty_print_json(data):
    pretty_print_json(json.dumps(data, indent=4, sort_keys=True))

@bot.message_handler(content_types=["text", "photo"])
def echo_all(message: Message):
    try:
        photo = message.photo[-1]
        id = message.caption
        if not id:
            raise Exception("No id provided")
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        handle_image(id, downloaded_file)
    except Exception as e:
         bot.reply_to(message, f"Error saving image, {e}")

def handle_image(id, downloaded_file):
    # Save the image locally
    # with open(f"{id}.jpg", 'wb') as new_file:
    #         new_file.write(downloaded_file)

    # print(f"Image saved as {id}.jpg")

    # Save the image on github
    repo.create_file(f"images/{id}.jpg","Added Image", downloaded_file, branch='main')
    pass


def signal_handler(sig, frame):
    print('Gracefully shutting down...')
    bot.stop_polling()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print("Bot started")
bot.infinity_polling()
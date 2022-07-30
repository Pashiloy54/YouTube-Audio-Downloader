from os import environ, walk, remove

import telebot
from pytube import YouTube, exceptions
from dotenv import load_dotenv

load_dotenv("config.env")

bot = telebot.TeleBot(environ['TOKEN'])


def get_file_audio(path="."):
    for root, dirs, files in walk(path):
        for file_name in files:
            if file_name.split(".")[1] == "mp4":
                return file_name


def download_audio(link, path="."):
    yt = YouTube(link)
    yt = yt.streams.get_audio_only()
    yt.download(path)


def send_audio(message, name_file):
    audio = open(name_file, 'rb')
    try:
        bot.send_audio(message.chat.id, audio)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, "The file is too huge Telegram can't send that much!")

    audio.close()
    remove(name_file)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message,
                 "/download_audio [link - insert a link to the video here]\n\n"
                 "\t\t\t\t\t\t\t\t!!!\t\t\t\t\t\t\t\tDon't send too huge videos\t\t\t\t\t\t\t\t!!!")


@bot.message_handler(commands=['download_audio'])
def main(message):
    bot.reply_to(message, "Wait a second...")
    try:
        download_audio(message.text.split()[1])
        send_audio(message, get_file_audio())
    except (exceptions.RegexMatchError, IndexError):
        bot.send_message(message.chat.id, "There is no such video!")


bot.infinity_polling()

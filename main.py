import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

TOKEN ='6903346134:AAFVD5vdQDRZ5hZ6m1LlBj2C14Y5PeS6HsQ'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    with open("users.txt","a") as f:
        f.write(str(cid)+"\n")
    bot.send_message(cid,"تشکر chat id شما ثبت شد")
    
@bot.message_handler(func=lambda m :True)
def sabt_cid(m):
    cid = m.chat.id
    with open("users.txt","a") as f:
        f.write(str(cid)+"\n")
    bot.send_message(cid,"تشکر chat id شما ثبت شد")

bot.infinity_polling()
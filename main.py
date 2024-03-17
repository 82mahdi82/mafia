import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import instalod
import os
import database

database.creat_database_tables()


TOKEN ='6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'

chanel_id=-1001850347734
userStep={}


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0

def name_media(folder_path,type):
    jpg_files = []
    # Loop through all files in the folder
    if type == "p":
        for file_name in os.listdir(folder_path):
            # Check if the file has .jpg extension
            if file_name.lower().endswith('.mp4'):
                jpg_files.append(os.path.join(folder_path, file_name))
            if file_name.lower().endswith('.jpg'):
                # If it does, add its full name to the list
                jpg_files.append(os.path.join(folder_path, file_name))
        return jpg_files
    
    else:
        for file_name in os.listdir(folder_path):
            # Check if the file has .jpg extension
            if file_name.lower().endswith('.mp4'):
                return [os.path.join(folder_path, file_name)]
            if file_name.lower().endswith('.jpg'):
                # If it does, add its full name to the list
                jpg_files.append(os.path.join(folder_path, file_name))
        return jpg_files

# folder_path = "/path/to/your/folder"  # آدرس فولدر مورد نظر خود را وارد کنید
# jpg_files = find_jpg_files(folder_path)
# for file_path in jpg_files:
#     print(file_path)




def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        print(m)
        cid = m.chat.id
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + "New photo recieved")
        elif m.content_type == 'document':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + 'New Document recieved')

bot = telebot.TeleBot(TOKEN,)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid=m.chat.id
    name=m.chat.first_name
    bot.send_message(cid,f"""
 سلام {name} عزیز به ربات اینستا دانلودر خوش اومدی.

با این ربات به راحتی میتونی ویدیو، پست ها و تصاویر رو از اینستاگرام دانلود کنی 

فقط لینک چیزی که میخوای دانلود کنی رو واسم بفرست                 
""")
    userStep[cid]=1


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def handler_serch_message(m):
    cid=m.chat.id
    text=m.text
    if "https://www.instagram.com/" in text:
        type=text.split("/")[3]
        media_id=text.split("/")[4]
        print(type)
        print(media_id)
        check=database.use_media(media_id)
        if len(check)==0:
            instalod.download_post(media_id)
            list_name=name_media(media_id,type)
            for i in list_name:
                with open(i, 'rb') as photo:  # مسیر فایل عکس
                    message=bot.send_photo(chanel_id, photo)
                print(message)
                database.insert_media(media_id,message.message_id)
                bot.forward_message(cid,chanel_id,message.message_id)
            os.rmdir(media_id)
        else:
            bot.forward_message(cid,chanel_id,check[0][1])
    else:
        bot.send_message(cid,"لینک ارسال شده معتبر نمیباشد لطفا لینک معتبری ارسال کنید")
        
bot.infinity_polling()
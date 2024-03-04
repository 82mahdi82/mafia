import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import database
import time
import datetime
import threading
import pytz
import terikh
import jdatetime

database.creat_database_tables()

TOKEN ='6903346134:AAFVD5vdQDRZ5hZ6m1LlBj2C14Y5PeS6HsQ'#'6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'

userStep = {} 
owner=[]
admin=[]#[6926746273]
geam_info={} #cid:{name:...,}
game_info_in_group={}
mid_game_in_group={}#gid:{number:[cid,name,mid]}
present_dict={}
temporary_time={}
change_nazer_or_senario={}#cid:[gid,mid]
start_game={}#cid:{gid:,mid:,url:,room_num:,room_pass:}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0

def gen_number_markup(qty):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'number_{max(qty-1, 1)}'),
               InlineKeyboardButton(f'{qty}', callback_data='number'),
               InlineKeyboardButton('➕', callback_data=f'number_{qty+1}'))
    markup.add(InlineKeyboardButton('تایید ✅', callback_data=f'number_add_{qty}'))
    return markup
def gen_number_markup_change(qty):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'number_change_{max(qty-1, 1)}'),
               InlineKeyboardButton(f'{qty}', callback_data='number'),
               InlineKeyboardButton('➕', callback_data=f'number_change_{qty+1}'))
    markup.add(InlineKeyboardButton('تایید ✅', callback_data=f'number_change_add_{qty}'))
    return markup

def is_bot_admin(chat_id):
    bot_member = bot.get_chat_member(int(chat_id), bot.get_me().id)
    if bot_member.status == 'administrator':
        return True
    else:
        return False
    
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m.chat.type)
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


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(func=lambda m: m.text=="کنسل")
def cancel_admin(m):
    command_start(m)




@bot.callback_query_handler(func=lambda call: call.data.startswith("cagame"))
def stgame_def(call):
    cid = call.message.chat.id
    mid=call.message.message_id
    start_game.pop(cid)
    bot.send_message(cid,"عملیات با موفقیت لغو شد")
    cancel_admin(call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("stgame"))
def stgame_def(call):
    cid = call.message.chat.id
    mid=call.message.message_id
    mid_game=int(start_game[cid]["mid"])
    gid=int(start_game[cid]["gid"])
    group_name = game_info_in_group[gid]["name"]
    # new_group = bot.create_chat(title=group_name, type='supergroup')
    # bot.create_chat_invite_link(cid,"mahdi")
    for i in mid_game_in_group[gid]:
        bot.send_message(mid_game_in_group[gid][i][0],f"""
لینک مستقیم ورود به اتاق : {start_game[cid]["url"]}
شماره اتاق : {start_game[cid]["room_num"]}
رمز اتاق : {start_game[cid]["room_pass"]}
""") 
    total_number_reserv=[] 
    # all_cid_reserv=all_cid_reserv.pop(cid)
    # mid_game_in_group[gid].pop(int(all_cid_reserv))
    text=""
    for i in mid_game_in_group[gid]:
        total_number_reserv.append(i)
        name=mid_game_in_group[gid][i][1]
        if mid_game_in_group[gid][i][0] in present_dict[gid]:
            text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
        else:
            text+=str(i)+"."+str(name)+"\n"
        bot.edit_message_caption(
f"""
📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
🕰ساعت شروع:{game_info_in_group[gid]["time"]}
👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
{text}
~~~~~~~~~~~~~~~~~~
بازی شروع شد
""",gid,mid_game,parse_mode="HTML"
                )
        mid_game_in_group.pop(gid)
        game_info_in_group.pop(gid)
        present_dict.pop(gid)
        start_game.pop(cid)

@bot.callback_query_handler(func=lambda call: call.data.startswith("meadmin"))
def menoadmin(call):
    cid=call.from_user.id
    command_start(call.message)
@bot.message_handler(content_types=["photo"])
def photo_handler(m):
    cid=m.chat.id
    if get_user_step(cid)==3:
        geam_info[cid].setdefault("photo",m.photo[0].file_id)
        bot.send_message(cid,"لطفا تعداد نفرات شرکت کننده در بازی را مشخص کنید ",reply_markup=gen_number_markup(1))





@bot.callback_query_handler(func=lambda call: call.data.startswith("deluser"))
def set_date(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    if cid in admin:
        userStep[cid]=500
        bot.answer_callback_query(call.id,"برای حذف کاربر از بازی روی شماره ای که میخواهید حذف کنید کلیک کنید")
    else:
        bot.answer_callback_query(call.id,"این قابلیت برای ادمین است")
@bot.callback_query_handler(func=lambda call: call.data.startswith("date"))
def set_date(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    data=call.data.split("_")
    bot.send_message(cid,
f"""
{data[1]}  {data[2]}
لطفا ساعت شروع بازی را در تاریخ درج شده در بالا با فرمت (00:00) وارد کنید
""")
    temporary_time.setdefault(cid,"")
    temporary_time[cid]=data[2]
    if len(data)==4:
        userStep[cid]=14
    else:
        userStep[cid]=5
@bot.callback_query_handler(func=lambda call: call.data.startswith("present"))
def present_def(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    if len(mid_game_in_group[gid])>0:
        list_cid=[]
        for i in mid_game_in_group[gid]:
            list_cid.append(mid_game_in_group[gid][i][0])
        if cid in list_cid:
            try:
                time_send=jdatetime.datetime.strptime(game_info_in_group[gid]["time"], "%H:%M %Y/%m/%d")-datetime.timedelta(minutes=15)
                ir_tz = pytz.timezone('Asia/Tehran')
                time2 = datetime.datetime.strftime(datetime.datetime.now(ir_tz),"%H:%M %Y/%m/%d")
                time3=datetime.datetime.strptime(time2,"%H:%M %Y/%m/%d")
                if time_send<=time3:
                    present_dict.setdefault(gid,[])
                    if cid not in present_dict[gid]:
                        present_dict[gid].append(cid)
                        bot.answer_callback_query(call.id,"حضور شما ثبت شد")
                        text=""
                        total_number_reserv=[]
                        for i in mid_game_in_group[gid]:
                            total_number_reserv.append(i)
                            name=mid_game_in_group[gid][i][1]
                            if mid_game_in_group[gid][i][0] in present_dict[gid]:
                                text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                            else:
                                text+=str(i)+"."+str(name)+"\n"
                        markup=InlineKeyboardMarkup()
                        markup_button=[]
                        for i in range(1,int(game_info_in_group[gid]["number"])+1):
                            if i in total_number_reserv:
                                markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
                            else:
                                markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
                        markup.add(*markup_button)
                        markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
                        # markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_change_senario_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_change_nazer_{game_info_in_group[gid]['gruop_id']}"))
                        # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{mid}"))
                        markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{mid}"))
                        markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
                        markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
                        bot.edit_message_caption(
f"""
📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
🕰ساعت شروع:{game_info_in_group[gid]["time"]}
👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
{text}
~~~~~~~~~~~~~~~~~~
""",gid,mid,parse_mode="HTML",reply_markup=markup
            )
                    else:
                        bot.answer_callback_query(call.id,"شما حضور خود را ثبت کرده اید")
                else:
                    bot.answer_callback_query(call.id,"هنوز زمان برای ثبت حضور نرسیده است")
            except:
                bot.answer_callback_query(call.id,"هنوز زمان برای ثبت حضور نرسیده است")
        else:
            bot.answer_callback_query(call.id,"شما در بازی نیستید")
    else:
        bot.answer_callback_query(call.id,"شما در بازی نیستید")




@bot.callback_query_handler(func=lambda call: call.data.startswith("sobjoin"))
def sobjoin_admin(call):
    cid= call.message.chat.id
    mid=call.message.message_id
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("کنسل")
    bot.send_message(cid,"لطفا نام کاربری شخصی که میخواهید او را ادمین کنید وارد کنید:",reply_markup=markup)
    userStep[cid]=300
@bot.callback_query_handler(func=lambda call: call.data.startswith("chanel"))
def select_chanel_new(call):
    cid= call.message.chat.id
    data=call.data.split("_")
    mid=call.message.message_id
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("کنسل")
    bot.send_message(cid,"برای اضافه کردن یک کانال لطفا ابتدا ربات را در آن کانال اد و ادمین کنید سپس یک پیام از همان کانال را در اینجا فوروارد کنید\nدر صورت لغو عملیات از دکمه کنسل استفاده کنید.",reply_markup=markup)
    userStep[cid]=200
@bot.callback_query_handler(func=lambda call: call.data.startswith("seting"))
def select_chanel(call):
    cid= call.message.chat.id
    data=call.data.split("_")[1]
    mid=call.message.message_id
    tuple_game=database.use_games(cid)[int(data)]
    geam_info.setdefault(cid,{})
    geam_info[cid]={"name":tuple_game[0],"photo":tuple_game[2],"number":tuple_game[3],"link_info":tuple_game[1],"time":tuple_game[4],"gruop_id":tuple_game[5],"gruop_name":tuple_game[6],"nazer":tuple_game[7],"name_nazer":tuple_game[8]}
    select_chanel_and_check(call)
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def select_chanel(call):
    cid= call.message.chat.id
    data=call.data.split("_")[1]
    mid=call.message.message_id
    tuple_game=database.use_games(cid)[int(data)]
    database.delete_games(tuple_game[0],tuple_game[1],tuple_game[9])
    bot.delete_message(cid,mid)
    bot.answer_callback_query(call.id,"بازی حذف شد")
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("list"))
def select_chanel(call):
    cid= call.message.chat.id
    if cid not in admin:
        return
    list_game=database.use_games(cid)
    if len(list_game)>0:
        total_num=0
        for i in list_game:
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("حذف",callback_data=f"delete_{total_num}"))
            markup.add(InlineKeyboardButton("تنظیمات",callback_data=f"seting_{total_num}_0"))
            bot.send_photo(cid,i[2],
f"""
📜سناریو:  <a href='{i[1]}'>{i[0]}</a>
🕰ساعت شروع:{i[4]}
👥نام گروه :{i[6]}
🎩ناظر:<a href='https://t.me/{i[7].replace("@","")}'>{i[8]}</a>
تعداد بازیکنان :{i[3]}
""",parse_mode="HTML",reply_markup=markup)
            total_num+=1
           
    else:
        bot.answer_callback_query(call.id,"شما هنوز بازی ذخیره نکرده اید")

@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel"))
def select_chanel(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    all_cid_reserv={}
    if gid in mid_game_in_group:
        if len(mid_game_in_group[gid])>0:
            for i in mid_game_in_group[gid]:
                all_cid_reserv.setdefault(mid_game_in_group[gid][i][0],i)
            if cid in all_cid_reserv:
                total_number_reserv=[] 
                all_cid_reserv=all_cid_reserv.pop(cid)
                mid_game_in_group[gid].pop(int(all_cid_reserv))
                text=""
                for i in mid_game_in_group[gid]:
                    total_number_reserv.append(i)
                    name=mid_game_in_group[gid][i][1]
                    if mid_game_in_group[gid][i][0] in present_dict[gid]:
                        text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                    else:
                        text+=str(i)+"."+str(name)+"\n"
                markup=InlineKeyboardMarkup()
                markup_button=[]
                for i in range(1,int(game_info_in_group[gid]["number"])+1):
                    if i in total_number_reserv:
                        markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
                    else:
                        markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
                markup.add(*markup_button)
                markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
                markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{mid}"))
                # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{mid}"))
                markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}_{mid}"))
                markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
                bot.edit_message_caption(
    f"""
    📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
    🕰ساعت شروع:{game_info_in_group[gid]["time"]}
    👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
    🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
    👤کسانی که جوین شدند:
    ~~~~~~~~~~~~~~~~~~
    {text}
    ~~~~~~~~~~~~~~~~~~
    """,gid,mid,reply_markup=markup,parse_mode="HTML"
                )
                bot.answer_callback_query(call.id,"انصراف شما انجام شد")
            else:
                bot.answer_callback_query(call.id,"شما در بازی رزرو نیستید")
        else:
            bot.answer_callback_query(call.id,"شما در بازی رزرو نیستید")
    else:
        bot.answer_callback_query(call.id,"شما در بازی رزرو نیستید")

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin"))
def select_chanel(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    data=call.data.split("_")
    if data[1]=="cancel":
        if cid in admin:
            bot.delete_message(gid,mid)
            game_info_in_group.pop(gid)
            mid_game_in_group.pop(gid)
            present_dict.pop(gid)
            bot.answer_callback_query(call.id,"بازی حذف شد")
        else:
            bot.answer_callback_query(call.id,"این قابلیت برای ادمین است")
    elif data[1]=="start":
        if cid in admin:
            if gid in mid_game_in_group:
                if len(mid_game_in_group[gid])>0:
                    markup=ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add("کنسل")
                    bot.send_message(cid,"لطفا برای شروع بازی لینکی را که میخواهید برای کاربران ارسال کنید را وارد کنید(URL) \nو در غیر این صورت دکمه کنسل را بزنید")
                    userStep[cid]=800
                    start_game.setdefault(cid,{})
                    start_game[cid]={"gid":data[2],"mid":mid}
                    bot.answer_callback_query(call.id,"برای شروع بازی وارد ربات شوید و مراحل را تکمیل کنید")
    #                 group_name = game_info_in_group[gid]["name"]
    #                 # new_group = bot.create_chat(title=group_name, type='supergroup')
    #                 # bot.create_chat_invite_link(cid,"mahdi")
    #                 for i in mid_game_in_group[gid]:
    #                     bot.send_message(mid_game_in_group[gid][i][0],f"لینک ورود به بازی برای شروع بازی روی لینک زیر بزنید \n{game_info_in_group[gid]["link_srart_game"]}")


    #                 total_number_reserv=[] 
    #                 # all_cid_reserv=all_cid_reserv.pop(cid)
    #                 # mid_game_in_group[gid].pop(int(all_cid_reserv))
    #                 text=""
    #                 for i in mid_game_in_group[gid]:
    #                     total_number_reserv.append(i)
    #                     name=mid_game_in_group[gid][i][1]
    #                     if mid_game_in_group[gid][i][0] in present_dict[gid]:
    #                         text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
    #                     else:
    #                         text+=str(i)+"."+str(name)+"\n"

    #                 bot.edit_message_caption(
    # f"""
    # 📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
    # 🕰ساعت شروع:{game_info_in_group[gid]["time"]}
    # 👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
    # 🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
    # 👤کسانی که جوین شدند:
    # ~~~~~~~~~~~~~~~~~~
    # {text}
    # ~~~~~~~~~~~~~~~~~~
    # بازی شروع شد
    # """,gid,mid,parse_mode="HTML"
    #                 )
    #                 mid_game_in_group.pop(gid)
    #                 game_info_in_group.pop(gid)
    #                 present_dict.pop(gid)
                else:
                    bot.answer_callback_query(call.id,"هنوز هیچ شرکت کننده ای برای شروع بازی وجود ندارد")
            else:
                bot.answer_callback_query(call.id,"هنوز هیچ شرکت کننده ای برای شروع بازی وجود ندارد")
        else:
            bot.answer_callback_query(call.id,"این قابلیت برای ادمین است")
    elif data[1]=="senario":
        if cid in admin:
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("کنسل")
            bot.send_message(cid,"لطفا برای تغییر سناریو اسم سناریو و لینک توضیحات را مانند نمونه ارسال کنید \nاسم سناریو***لینک توضیحات",reply_markup=markup)
            change_nazer_or_senario.setdefault(cid,[])
            change_nazer_or_senario[cid]=[data[2],data[3]]
            userStep[cid]=400
            bot.answer_callback_query(call.id,"لطفا برای انجام تغییر وارد ربات شوید و مراحل را طی کنید")

        else:
            bot.answer_callback_query(call.id,"این قابلیت برای ادمین است")
            
    elif data[1]=="nazer":
        if cid in admin:
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("کنسل")
            bot.send_message(cid,"لطفا برای تغییر ناظر یوزرنیم ناظر و اسم ناظر را مانند نمونه ارسال کنید \nیوزرنیم***اسم ناظر",reply_markup=markup)
            change_nazer_or_senario.setdefault(cid,[])
            change_nazer_or_senario[cid]=[data[2],data[3]]
            userStep[cid]=401
            bot.answer_callback_query(call.id,"لطفا برای انجام تغییر وارد ربات شوید و مراحل را طی کنید")

        else:
            bot.answer_callback_query(call.id,"این قابلیت برای ادمین است")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reserv"))
def select_chanel(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    data=call.data.split("_")[-1]
    if data=="ok":
        if cid in admin:
            if userStep[cid]==500:
                number=int(call.data.split("_")[1])
                mid_game_in_group[gid].pop(number)
                total_number_reserv=[] 
                text=""
                for i in mid_game_in_group[gid]:
                    total_number_reserv.append(i)
                    name=mid_game_in_group[gid][i][1]
                    if mid_game_in_group[gid][i][0] in present_dict[gid]:
                        text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                    else:
                        text+=str(i)+"."+str(name)+"\n"
                markup=InlineKeyboardMarkup()
                markup_button=[]
                for i in range(1,int(game_info_in_group[gid]["number"])+1):
                    if i in total_number_reserv:
                        markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
                    else:
                        markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
                markup.add(*markup_button)
                markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
                # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{mid}"))
                markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{mid}"))
                markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
                markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
                bot.edit_message_caption(
f"""
📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
🕰ساعت شروع:{game_info_in_group[gid]["time"]}
👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
{text}
~~~~~~~~~~~~~~~~~~
""",gid,mid,reply_markup=markup,parse_mode="HTML"
                )
                userStep[cid]=0
                bot.answer_callback_query(call.id,"بازیکن حذف شد")
                return
            else:
                bot.answer_callback_query(call.id,"این شماره قبلا رزرو شده است")
                return
        else:
            bot.answer_callback_query(call.id,"این شماره قبلا رزرو شده است")
            return
    else:
        if cid in userStep:
            if userStep[cid]==500:
                bot.answer_callback_query(call.id,"در این شماره بازیکنی برای حذف کردن وجود ندارد")
                userStep[cid]=0
                return
        list_user_login=database.use_users()
        list_cid_user={}
        for i in list_user_login:
            list_cid_user.setdefault(i[0],i[1])  
        if cid in list_cid_user:
            total_number_reserv=[]
            all_cid_reserv=[]
            mid_game_in_group.setdefault(gid,{})
            if len(mid_game_in_group[gid])>0:
                for i in mid_game_in_group[gid]:
                    all_cid_reserv.append(mid_game_in_group[gid][i][0])
            if cid not in all_cid_reserv:
                time_send=jdatetime.datetime.strptime(game_info_in_group[gid]["time"], "%H:%M %Y/%m/%d")-datetime.timedelta(minutes=15)
                ir_tz = pytz.timezone('Asia/Tehran')
                time2 = datetime.datetime.strftime(datetime.datetime.now(ir_tz),"%H:%M %Y/%m/%d")
                time3=datetime.datetime.strptime(time2,"%H:%M %Y/%m/%d")
                if time_send<=time3:
                    present_dict[gid].append(cid)
                mid_game_in_group[gid].setdefault(int(data),[cid,list_cid_user[cid],mid])
                text=""
                for i in mid_game_in_group[gid]:
                    total_number_reserv.append(i)
                    name=mid_game_in_group[gid][i][1]
                    if mid_game_in_group[gid][i][0] in present_dict[gid]:
                        text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                    else:
                        text+=str(i)+"."+str(name)+"\n"
                markup=InlineKeyboardMarkup()
                markup_button=[]
                for i in range(1,int(game_info_in_group[gid]["number"])+1):
                    if i in total_number_reserv:
                        markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
                    else:
                        markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
                markup.add(*markup_button)

                markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
                # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{mid}"))
                markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{mid}"))
                markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
                markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
                bot.edit_message_caption(
    f"""
    📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
    🕰ساعت شروع:{game_info_in_group[gid]["time"]}
    👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
    🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
    👤کسانی که جوین شدند:
    ~~~~~~~~~~~~~~~~~~
    {text}
    ~~~~~~~~~~~~~~~~~~
    """,gid,mid,reply_markup=markup,parse_mode="HTML"
                )
                # if len(total_number_reserv)==int(game_info_in_group[gid]["number"]):


            else:
                bot.answer_callback_query(call.id,"شما قبلا در این بازی رزور شده اید")
        else:
            bot.answer_callback_query(call.id,"لطفا با استفاده از دکمه ثبت نام وارد ربات شوید و ثبت نام کنید")




@bot.callback_query_handler(func=lambda call: call.data.startswith("login"))
def select_user_name_for(call):
    cid = call.message.chat.id
    bot.send_message(cid,"لطفا نام کاربری خود را وارد کنید:")
    userStep[cid]=20

# @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm"))
# def select_chanel(call):
#     cid = call.message.chat.id
#     if int(geam_info[cid]["gruop_id"]) not in game_info_in_group:
#         bot.send_message(cid,"لطفا یک گروه بسازید و لینک گروه را برای پس از شروع بازی و جوین شدن کاربران ارسال کنید:")
#         userStep[cid]=700
#     else:
#         bot.answer_callback_query(call.id,"در این کانال/گروه در حال حاضر یک بازی در حال اجرا است لطفا یک کانال/گروه دیگر را انتخاب کنید")
#         creat_geam_3(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm"))
def select_chanel(call):
    cid = call.message.chat.id
    userStep[cid]=0
    if int(geam_info[cid]["gruop_id"]) not in game_info_in_group:
        markup=InlineKeyboardMarkup()
        markup_button=[]
        for i in range(1,int(geam_info[cid]["number"])+1):
            markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
        markup.add(*markup_button)
        markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{geam_info[cid]['gruop_id']}"))
        markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_change_nazer_{geam_info[cid]['gruop_id']}"))
        # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario {gid} {mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer {gid} {mid}"))
        markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{geam_info[cid]['gruop_id']}"))
        markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
        mmessege=bot.send_photo(geam_info[cid]["gruop_id"],geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~
""",parse_mode='HTML',reply_markup=markup)
        markup2=InlineKeyboardMarkup()
        markup_button=[]
        for i in range(1,int(geam_info[cid]["number"])+1):
            markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
        markup2.add(*markup_button)
        markup2.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{geam_info[cid]['gruop_id']}"))
        # markup2.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_change_senario_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_change_nazer_{geam_info[cid]['gruop_id']}"))
        # markup2.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"))
        # markup2.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"))
        markup2.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"))
        markup2.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{geam_info[cid]['gruop_id']}_{mmessege.message_id}"))
        markup2.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
        bot.edit_message_caption(
f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~
""",geam_info[cid]["gruop_id"],mmessege.message_id,parse_mode='HTML',reply_markup=markup2
        )
        userStep[cid]=0
        game_info_in_group.setdefault(int(geam_info[cid]["gruop_id"]),{})
        game_info_in_group[int(geam_info[cid]["gruop_id"])]=geam_info[cid]
        game_info_in_group[int(geam_info[cid]["gruop_id"])].setdefault("mid",mmessege.message_id)
        present_dict.setdefault(int(geam_info[cid]["gruop_id"]),[])
        game_info_in_group.setdefault(int(geam_info[cid]["gruop_id"]),{})
        mid_game_in_group.setdefault(int(geam_info[cid]["gruop_id"]),{})
        geam_info.pop(cid)
        bot.answer_callback_query(call.id,"بازی در کانال/گروه ارسال شد")
    else:
        bot.answer_callback_query(call.id,"در این کانال/گروه در حال حاضر یک بازی در حال اجرا است لطفا یک کانال/گروه دیگر را انتخاب کنید")
        creat_geam_3(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("change"))
def select_chanel(call):
    cid = call.message.chat.id
    data= call.data.split("_")[-1]
    if data=="scenario":
        bot.send_message(cid,"اسم سناریو بازی را ارسال کنید:")
        userStep[cid]=11
    elif data=="link":
        bot.send_message(cid,"لینک توضیح سناریو بازی را وارد کنید:")
        userStep[cid]=12
    elif data=="number":
        bot.send_message(cid,"تعداد نفرات شرکت کننده در بازی را وارد کنید:",reply_markup=gen_number_markup_change(int(geam_info[cid]["number"])))
        userStep[cid]=13
    elif data=="time":
        dict_weak=terikh.dict_time_now()
        markup=InlineKeyboardMarkup()
        for i in dict_weak:
            markup.add(InlineKeyboardButton(f"{i} {dict_weak[i]}",callback_data=f"date_{i}_{dict_weak[i]}_0"))
        # markup.add(InlineKeyboardButton("به محض تکمیل لیست",callback_data="complete_list"))
        bot.send_message(cid,"لطفا زمان شروع بازی را مشخص کنید ",reply_markup=markup)
        # bot.send_message(cid,"تایم شروع بازی را وارد کنید (فرمت 00:00):")
        # userStep[cid]=14
    elif data=="group":
        list_dict_grups=database.use_table_admin_group(cid)
        markup=InlineKeyboardMarkup()
        for i in list_dict_grups:
            markup.add(InlineKeyboardButton(i[1],callback_data=f"select_ghange_{i[0]}_{i[1]}"))
        bot.send_message(cid,"گروهی که میخواهید بازی در آن ارسال شود را انتخاب کنید",reply_markup=markup)
        userStep[cid]=15
    elif data=="nazer":
        bot.send_message(cid,"یوزر ناظر به همراه اسم ناظر را مانند نمونه ارسال کنید(@nazer ناظر)")
        userStep[cid]=16

    


@bot.callback_query_handler(func=lambda call: call.data.startswith("complete_list"))
def select_chanel(call):
    cid = call.message.chat.id
    text="به محض تکمیل لیست"
    geam_info.setdefault(cid,{})
    geam_info[cid].setdefault("time",text)
    markup=InlineKeyboardMarkup()
    list_dict_grups=database.use_table_admin_group(cid)
    grup_ok=False
    if len(list_dict_grups)>0:
        for i in list_dict_grups:
            if is_bot_admin(i[0]):
                markup.add(InlineKeyboardButton(i[1],callback_data=f"select_{i[0]}_{i[1]}"))
                grup_ok=True
    else:
        markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"ربات شما در گروهی عضو نیست لطفا برای ارسال بازی در گروه ربات را در آن گروه اد کنید و ادمین کنید.\nسپس دکمه سرچ را بزنید.\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
        userStep[cid]=0
        return
    if grup_ok:
        markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"لطفا گروهی که میخواهید بازی در آن ارسال شود را انتخاب کنید:\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"لطفا ربات را در گروه هایی که میخواهید بازی را ارسال کنید ادمین کنید.\nسپس دکمه سرچ را بزنید\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
    userStep[cid]=0

@bot.callback_query_handler(func=lambda call: call.data.startswith("adding"))
def adding(call):
    cid = call.message.chat.id
    try:
        database.insert_games(geam_info[cid]["name"],geam_info[cid]["link_info"],geam_info[cid]["photo"],int(geam_info[cid]["number"]),geam_info[cid]["time"],geam_info[cid]["gruop_id"],geam_info[cid]["gruop_name"],geam_info[cid]["nazer"],geam_info[cid]["name_nazer"],cid)
        bot.answer_callback_query(call.id,"بازی در حافظه ذخیره شد")
    except:
       bot.answer_callback_query(call.id,"قبلا بازی با این لینک ذخیره کرده اید لطفا برای ثبت بازی جدید با همین لینک بازی قبلی را حذف کنید")

@bot.callback_query_handler(func=lambda call: call.data.startswith("select"))
def select_chanel_and_check(call):
    cid = call.message.chat.id
    data=call.data.split("_")
    # geam_info.setdefault("")
    if len(data)==4:
        geam_info[cid]["gruop_name"]=data[-1]
        geam_info[cid]["gruop_id"]=data[-2]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
        markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
        markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
        markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
        markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
        markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
        markup.add(InlineKeyboardButton("اضافه کردن بازی به حافظه",callback_data="adding"))
        markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
        bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)
        userStep[cid]=0

    elif len(data)==3:
        geam_info[cid].setdefault("gruop_name",data[-1])
        geam_info[cid].setdefault("gruop_id",data[1])
        # database.insert_games(geam_info[cid]["name"],geam_info[cid]["link_info"],geam_info[cid]["photo"],int(geam_info[cid]["number"]))
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
        markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
        markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
        markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
        markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
        markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
        markup.add(InlineKeyboardButton("اضافه کردن بازی به حافظه",callback_data="adding"))
        markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
        bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("again"))
def again_chanel(call):
    cid = call.message.chat.id
    creat_geam_3(call.message)
@bot.callback_query_handler(func=lambda call: call.data.startswith("creat"))
def creat_senaryo(call):
    cid = call.message.chat.id
    if cid not in admin:
        return
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("کنسل")
    bot.send_message(cid,"لطفا نام سناریو بازی را ارسال کنید:",reply_markup=markup)
    userStep[cid]=1


@bot.callback_query_handler(func=lambda call: call.data.startswith("number"))
def call_callback_data_number(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    if len(data)==2:
        bot.edit_message_reply_markup(cid,mid,reply_markup=gen_number_markup(int(data[-1])))
    elif len(data)==3 and data[1]=="add":
        geam_info[cid].setdefault("number",data[-1])
        bot.answer_callback_query(call.id,"تعداد ثبت شد")
        bot.send_message(cid,"لطفا آی دی ناظر را ارسال کنید:(مثال:@nazer)")
        userStep[cid]=4
    elif len(data)==3:
        bot.edit_message_reply_markup(cid,mid,reply_markup=gen_number_markup_change(int(data[-1])))
    elif len(data)==4:
        geam_info[cid]["number"]=int(data[3])
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
        markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
        markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
        markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
        markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
        markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
        markup.add(InlineKeyboardButton("اضافه کردن بازی به حافظه",callback_data="adding"))
        markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
        bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith("adelete"))
def call_callback_data_number(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    adminid = int(call.data.split("_")[1])
    admin.remove(adminid)
    bot.delete_message(cid,mid)
    bot.answer_callback_query(call.id,"ادمین حذف شد")


@bot.callback_query_handler(func=lambda call: call.data.startswith("logchang"))
def change_user_name(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    database.delete_user(cid)
    select_user_name_for(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("lisobjoin"))
def call_callback_data_number(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    if len(admin)-1>0:
        for i in admin:
            if i not in owner:
                username=database.use_users_admin(int(i))[0][1]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("حذف ادمین",callback_data=f"adelete_{i}"))
                bot.send_message(cid,f"نام کاربری ادمین: {username}",reply_markup=markup)
    else:
        bot.answer_callback_query(call.id,"شما فعلا ادمینی انتخاب نکرده اید")



@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def handle_new_member(m):
    # print(m)
    group_id = m.chat.id
    cid=m.from_user.id
    bot_info=bot.get_me()
    if m.new_chat_members[0].username==bot_info.username:
        try:
            database.insert_group(group_id,m.chat.title,cid)
        except:
            pass
        

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid in start_game:
        start_game.pop(cid)
    if cid in userStep:
        userStep[cid]=0
    if m.chat.type=="private":
        if cid in userStep:
            userStep[cid]=0
        if cid in change_nazer_or_senario:
            change_nazer_or_senario.pop(cid)
        if len(m.text.split(" "))==2 and m.text.split(" ")[1]!="login":
            if cid in admin:
                markup=ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("کنسل")
                if m.text.split(" ")[1].split("_")[0]=="senario":    
                    bot.send_message(cid,"لطفا برای تغییر سناریو اسم سناریو و لینک توضیحات را مانند نمونه ارسال کنید \nاسم سناریو***لینک توضیحات",reply_markup=markup)
                    change_nazer_or_senario.setdefault(cid,[])
                    change_nazer_or_senario[cid]=[m.text.split(" ")[1].split("_")[1],m.text.split(" ")[1].split("_")[2]]
                    userStep[cid]=400
                elif m.text.split(" ")[1].split("_")[0]=="nazer":
                    bot.send_message(cid,"لطفا برای تغییر ناظر یوزرنیم ناظر و اسم ناظر را مانند نمونه ارسال کنید \nیوزرنیم***اسم ناظر",reply_markup=markup)
                    change_nazer_or_senario.setdefault(cid,[])
                    change_nazer_or_senario[cid]=[m.text.split(" ")[1].split("_")[1],m.text.split(" ")[1].split("_")[2]]
                    userStep[cid]=401
            else:
                list_user_login=database.use_users()
                list_cid_user=[]
                for i in list_user_login:
                    list_cid_user.append(i[0])
                if cid not in list_cid_user:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("ثبت نام",callback_data="login"))
                    bot.send_message(cid,"لطفا برای بازی و استفاده از ربات ثبت نام کنید",reply_markup=markup)
                else:
                    bot.send_message(cid,"ثبت نام شما انجام شده و میتوانید در بازی ها شرکت کنید")

        else:
            # bot_member = bot.get_chat_member(chat_id, 6926746273)
            # print("staaaaaaaaaaaaatos",bot_member)
            if len(owner)==0:
                owner.append(cid)
                admin.append(cid)
            if cid in owner:
                if cid in geam_info:
                    geam_info.pop(cid)
                userStep[cid]=0
                list_user_login=database.use_users()
                list_cid_user=[]
                for i in list_user_login:
                    list_cid_user.append(i[0])
                if cid not in list_cid_user:   
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("ساخت بازی جدید",callback_data="creat_geam"))
                    markup.add(InlineKeyboardButton("لیست بازی های ذخیره شده",callback_data="list"))
                    markup.add(InlineKeyboardButton("افزودن ادمین",callback_data="sobjoin"))
                    markup.add(InlineKeyboardButton("لیست ادمین ها",callback_data="lisobjoin"))
                    markup.add(InlineKeyboardButton("ثبت نام به عنوان بازیکن",callback_data="login"))
                else:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("ساخت بازی جدید",callback_data="creat_geam"))
                    markup.add(InlineKeyboardButton("لیست بازی های ذخیره شده",callback_data="list"))
                    markup.add(InlineKeyboardButton("افزودن ادمین",callback_data="sobjoin"))
                    markup.add(InlineKeyboardButton("لیست ادمین ها",callback_data="lisobjoin"))
                    markup.add(InlineKeyboardButton("تغییر نام کاربری",callback_data="logchang")) 
                bot.send_message(cid,"""
        سلام مدیر گرامی به ربات خوش آمدید 
        لطفا برای استفاده از ربات از دکمه های زیر استفاده کنید
        """,reply_markup=markup)
            elif cid in admin:
                if cid in geam_info:
                    geam_info.pop(cid)
                userStep[cid]=0
                list_user_login=database.use_users()
                list_cid_user=[]
                for i in list_user_login:
                    list_cid_user.append(i[0])
                if cid not in list_cid_user:   
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("ساخت بازی جدید",callback_data="creat_geam"))
                    markup.add(InlineKeyboardButton("لیست بازی های ذخیره شده",callback_data="list"))
                    markup.add(InlineKeyboardButton("ثبت نام به عنوان بازیکن",callback_data="login"))
                else:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("ساخت بازی جدید",callback_data="creat_geam"))
                    markup.add(InlineKeyboardButton("لیست بازی های ذخیره شده",callback_data="list"))
                    markup.add(InlineKeyboardButton("تغییر نام کاربری",callback_data="logchang"))                

                bot.send_message(cid,"""
        سلام ادمین گرامی به ربات خوش آمدید 
        لطفا برای استفاده از ربات از دکمه های زیر استفاده کنید
        """,reply_markup=markup)
            else:
                list_user_login=database.use_users()
                list_cid_user=[]
                for i in list_user_login:
                    list_cid_user.append(i[0])
                if cid not in list_cid_user:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("ثبت نام",callback_data="login"))
                    bot.send_message(cid,"لطفا برای بازی و استفاده از ربات ثبت نام کنید",reply_markup=markup)
                else:
                    markup=InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("تغییر نام کاربری",callback_data="logchang"))
                    bot.send_message(cid,"ثبت نام شما انجام شده و میتوانید در بازی ها شرکت کنید",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def creat_geam_1(m):
    cid = m.chat.id
    text=m.text
    geam_info.setdefault(cid,{})
    geam_info[cid].setdefault('name',text)
    bot.send_message(cid,"لینک توضیحات سناریو بازی را ارسال کنید:")
    userStep[cid]=2


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==2)
def creat_geam_2(m):
    cid = m.chat.id
    text=m.text
    geam_info.setdefault(cid,{})
    geam_info[cid].setdefault('link_info',text)
    bot.send_message(cid,"لطفا برای بازی یک بنر ارسال کنید(عکس)")
    userStep[cid]=3
# @bot.message_handler(func=lambda m: get_user_step(m.chat.id)==4)
# def creat_geam_2(m):
#     cid = m.chat.id
#     text=m.text
#     geam_info.setdefault(cid,{})
#     geam_info[cid].setdefault('link_info',text)
#     bot.send_message(cid,"لطفا تعداد نفرات شرکت کننده در بازی را مشخص کنید ",reply_markup=gen_number_markup(1))

# @bot.message_handler(func=lambda m: get_user_step(m.chat.id)==3)
# def creat_geam_3(m):
#     cid = m.chat.id
#     text=m.text
#     bot.send_message(cid,"لطفا آی دی ناظر را ارسال کنید:(مثال:@nazer)")
#     userStep[cid]=4

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==4)
def creat_geam_4(m):
    cid = m.chat.id
    text=m.text
    geam_info.setdefault(cid,{})
    geam_info[cid].setdefault('nazer',text)
    bot.send_message(cid,"لطفا اسم ناظر را وارد کنید:")
    userStep[cid]=7

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==7)
def creat_geam_4(m):
    cid = m.chat.id
    text=m.text
    geam_info.setdefault(cid,{})
    geam_info[cid].setdefault('name_nazer',text)
    dict_weak=terikh.dict_time_now()
    markup=InlineKeyboardMarkup()
    for i in dict_weak:
        markup.add(InlineKeyboardButton(f"{i} {dict_weak[i]}",callback_data=f"date_{i}_{dict_weak[i]}"))
    # markup.add(InlineKeyboardButton("به محض تکمیل لیست",callback_data="complete_list"))
    bot.send_message(cid,"لطفا زمان شروع بازی را مشخص کنید ",reply_markup=markup)
    # userStep[cid]=5

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==5)
def creat_geam_3(m):
    cid = m.chat.id
    if get_user_step(cid)==5:
        try:
            text=m.text
            timmme=jdatetime.datetime.now().replace(day=int(temporary_time[cid].split("/")[2]), month=int(temporary_time[cid].split("/")[1]), hour=int(text.split(":")[0]), minute=int(text.split(":")[1]), second=0)
            geam_info.setdefault(cid,{})
            geam_info[cid].setdefault("time",f"{text} {temporary_time[cid]}")
            temporary_time.pop(cid)
        except:
            bot.send_message(cid,"فرمت زمان ارسال شده نا معتبر است لطفا زمان را به درستی وارد کنید")
            return

    markup=InlineKeyboardMarkup()
    list_dict_grups=database.use_table_admin_group(cid)
    grup_ok=False
    if len(list_dict_grups)>0:
        for i in list_dict_grups:
            if is_bot_admin(i[0]):
                markup.add(InlineKeyboardButton(i[1],callback_data=f"select_{i[0]}_{i[1]}"))
                grup_ok=True
    else:
        markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"ربات شما در گروهی عضو نیست لطفا برای ارسال بازی در گروه ربات را در آن گروه اد کنید و ادمین کنید.\nسپس دکمه سرچ را بزنید.\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
        userStep[cid]=0
        return
    if grup_ok:
        markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"لطفا گروهی که میخواهید بازی در آن ارسال شود را انتخاب کنید:\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"لطفا ربات را در گروه هایی که میخواهید بازی را ارسال کنید ادمین کنید.\nسپس دکمه سرچ را بزنید\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==11)
def creat_geam_1(m):
    cid = m.chat.id
    text=m.text
    geam_info[cid]["name"]=text
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
    markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
    markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
    markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
    markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
    markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
    markup.add(InlineKeyboardButton("اضافه کردن بازی به حافظه",callback_data="adding"))
    markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
    bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==12)
def creat_geam_1(m):
    cid = m.chat.id
    text=m.text
    geam_info[cid]["link_info"]=text
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
    markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
    markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
    markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
    markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
    markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
    markup.add(InlineKeyboardButton("اضافه کردن بازی به حافظه",callback_data="adding"))
    markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
    bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==14)
def creat_geam_1(m):
    cid = m.chat.id
    try:
        text=m.text
        timmme=jdatetime.datetime.now().replace(day=int(temporary_time[cid].split("/")[2]), month=int(temporary_time[cid].split("/")[1]), hour=int(text.split(":")[0]), minute=int(text.split(":")[1]), second=0)
        geam_info.setdefault(cid,{})
        geam_info[cid]["time"]=f"{text} {temporary_time[cid]}"
        temporary_time.pop(cid)
    except:
        bot.send_message(cid,"فرمت زمان ارسال شده نا معتبر است لطفا زمان را به درستی وارد کنید")
        return
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
    markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
    markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
    markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
    markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
    markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
    markup.add(InlineKeyboardButton("اضافه کردن بازی به حافظه",callback_data="adding"))
    markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
    bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==16)
def creat_geam_1(m):
    cid = m.chat.id
    text=m.text.split(" ")
    geam_info[cid]["nazer"]=text[0]
    geam_info[cid]["name_nazer"]=text[1]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تغیر سناریو",callback_data="change_scenario"))
    markup.add(InlineKeyboardButton("تغییر لینک توضیح سناریو",callback_data="change_link"))
    markup.add(InlineKeyboardButton("تغییر تعداد شرکت کندگان",callback_data="change_number"))
    markup.add(InlineKeyboardButton("تغییر ساعت ",callback_data="change_time"))
    markup.add(InlineKeyboardButton("تغییر گروه",callback_data="change_group"))
    markup.add(InlineKeyboardButton('تغییر ناظر',callback_data="change_nazer"))
    markup.add(InlineKeyboardButton("تایید و ارسال",callback_data="confirm"))
    bot.send_photo(cid,geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
""",parse_mode='HTML',reply_markup=markup)
    userStep[cid]=0


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==20)
def loging_cid(m):
    cid=m.chat.id
    text=m.text
    list_user_name=[]
    list_cid=[]
    list_all=database.use_users()
    for i in list_all:
        list_cid.append(i[0])
        list_user_name.append(i[1])
    if cid not in list_cid:
        if text not in list_user_name:
            database.insert_users(int(cid),text)
            if cid in admin:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("منو",callback_data="meadmin"))
                bot.send_message(cid,f"نام کاربری '{text}' برای شما تایید شد",reply_markup=markup)
            else:
                bot.send_message(cid,f"نام کاربری '{text}' برای شما تایید شد حالا میتوانید در بازی ها شرکت کنید")
            userStep[cid]=0
        else:
            bot.send_message(cid,"این نام کاربری قبلا انتخاب شده است لطفا نام کاربری دیگری را وارد کنید:")
    else:
        bot.send_message(cid,"شما قبلا ثبت نام کرده اید")

    # try:
    #     database.insert_users(int(cid),text)
    #     bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد شما حالا میتوانید در بازی ها شرکت کنید")
    # except:
    #     bot.send_message(cid,"شما قبلا ثبت نام کرده اید")

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==200)
def creat_geam_1(m):
    cid = m.chat.id
    text=m.text
    if m.forward_origin != None:
        if m.forward_origin.type=="channel":
            database.insert_group(m.forward_origin.chat.id,m.forward_origin.chat.title,cid)
            markup=InlineKeyboardMarkup()
            list_dict_grups=database.use_table_admin_group(cid)
            
            if len(list_dict_grups)>0:
                grup_ok=False
                for i in list_dict_grups:
                    if is_bot_admin(i[0]):
                        markup.add(InlineKeyboardButton(i[1],callback_data=f"select_{i[0]}_{i[1]}"))
                        grup_ok=True
                if grup_ok:
                    markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
                    markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
                    bot.send_message(cid,"لطفا گروهی که میخواهید بازی در آن ارسال شود را انتخاب کنید:\n\nو در صورتی که قصد دارید کانالی را اضافه کنید از دکمه 'افزودن کانال' استفاده کنید",reply_markup=markup)
                else:
                    markup.add(InlineKeyboardButton("افزودن کانال",callback_data="chanel"))
                    markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
                    bot.send_message(cid,"لطفا ربات را در کانال ها و گروه هایی که میخواید بازی را ارسال کنید ادمین کنید",reply_markup=markup)
        else:
            bot.send_message(cid,"لطفا پیامی را که فوروارد میکنید فقط از یک کانال باشد")
    else:
        bot.send_message(cid,"لطفا پیام را از کانالی فوروارد کنید")
    
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==300)
def add_new_admin(m):
    cid = m.chat.id
    text=m.text
    try:
        list_cid_user=database.use_users_user_name(text)
        admin.append(int(list_cid_user[0][0]))
        bot.send_message(cid,f"کاربر '{list_cid_user[0][1]}' به ادمین ارتقا یافت")
        bot.send_message(int(list_cid_user[0][0]),"درجه شما به ادمین ارتقا یافت")
        userStep[cid]=0
    except:
        bot.send_message(cid,"شخصی با این نام کاربری هنوز در ربات ثبت نام نکرده است.")

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==400)
def change_senario_or_nazer_def(m):
    cid = m.chat.id
    text=m.text
    gid=int(change_nazer_or_senario[cid][0])
    mid=int(change_nazer_or_senario[cid][1])
    if "***" in text:
        senario_name=text.split("***")[0]
        senario_link=text.split("***")[1]
        total_number_reserv=[]
        text2=""
        if gid in mid_game_in_group:
            if len(mid_game_in_group[gid])>0:
                
                for i in mid_game_in_group[gid]:
                    total_number_reserv.append(i)
                    name=mid_game_in_group[gid][i][1]
                    if mid_game_in_group[gid][i][0] in present_dict[gid]:
                        text2+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                    else:
                        text2+=str(i)+"."+str(name)+"\n"
        markup=InlineKeyboardMarkup()
        markup_button=[]
        for i in range(1,int(game_info_in_group[gid]["number"])+1):
            if i in total_number_reserv:
                markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
            else:
                markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
        markup.add(*markup_button)
        markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
        # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{mid}"))
        markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{mid}"))
        markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
        markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
        bot.edit_message_caption(
f"""
📜سناریو:  <a href='{senario_link}'>{senario_name}</a>
🕰ساعت شروع:{game_info_in_group[gid]["time"]}
👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
{text2}
~~~~~~~~~~~~~~~~~~
""",gid,mid,reply_markup=markup,parse_mode="HTML"
                )   
        change_nazer_or_senario.pop(cid) 
        game_info_in_group[gid]["link_info"]=senario_link
        game_info_in_group[gid]["name"]=senario_name
        userStep[cid]=0
        bot.send_message(cid,"سناریو بازی تغییر کرد")

    else:
        bot.send_message(cid,"لطفا مانند نمونه ارسال کنید")
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==401)
def change_senario_or_nazer_def(m):
    cid = m.chat.id
    text=m.text
    gid=int(change_nazer_or_senario[cid][0])
    mid=int(change_nazer_or_senario[cid][1])
    if "***" in text:
        user_name=text.split("***")[0]
        name_nazer=text.split("***")[1]
        total_number_reserv=[]
        text2=""
        if gid in mid_game_in_group:
            if len(mid_game_in_group[gid])>0:
                
                for i in mid_game_in_group[gid]:
                    total_number_reserv.append(i)
                    name=mid_game_in_group[gid][i][1]
                    if mid_game_in_group[gid][i][0] in present_dict[gid]:
                        text2+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                    else:
                        text2+=str(i)+"."+str(name)+"\n"
        markup=InlineKeyboardMarkup()
        markup_button=[]
        for i in range(1,int(game_info_in_group[gid]["number"])+1):
            if i in total_number_reserv:
                markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
            else:
                markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
        markup.add(*markup_button)
        markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
        # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{mid}"))
        markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{mid}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{mid}"))
        markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
        markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
        bot.edit_message_caption(
f"""
📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
🕰ساعت شروع:{game_info_in_group[gid]["time"]}
👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{user_name.replace("@","")}'>{name_nazer}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
{text2}
~~~~~~~~~~~~~~~~~~
""",gid,mid,reply_markup=markup,parse_mode="HTML"
                )    
        game_info_in_group[gid]["nazer"]=user_name
        game_info_in_group[gid]["name_nazer"]=name_nazer
        userStep[cid]=0
        bot.send_message(cid,"ناظر بازی تغییر کرد")
    else:
        bot.send_message(cid,"لطفا مانند نمونه ارسال کنید")



# @bot.message_handler(func=lambda m: get_user_step(m.chat.id)==700)
# def connfiirrmm(m):
#     cid = m.chat.id
#     text=m.text
#     geam_info[cid].setdefault("link_srart_game",text)
#     geam_info[cid]["link_srart_game"]=text
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("تایید لینک و ارسال بازی",callback_data="cconfirm"))
#     markup.add(InlineKeyboardButton("ارسال مجدد لینک",callback_data="confirm"))
#     bot.send_message(cid,"لینک دریافت شد اگر مورد تایید است دکمه تایید را بزنید",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==800)
def start_game_def1(m):
    cid = m.chat.id
    text=m.text
    start_game[cid].setdefault("url",text)
    bot.send_message(cid,"لطفا شماره اتاق را وارد کنید:(یک عدد چهار رقمی مثال:1234)")
    userStep[cid]=801

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==801)
def start_game_def2(m):
    cid = m.chat.id
    text=m.text
    start_game[cid].setdefault("room_num",text)
    bot.send_message(cid,"لطفا رمز اتاق را وارد کنید:(یک عدد چهار رقمی مثال:5678)")
    userStep[cid]=802

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==802)
def start_game_def3(m):
    cid = m.chat.id
    text=m.text
    start_game[cid].setdefault("room_pass",text)
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تایید و شروع بازی",callback_data="stgame"))
    markup.add(InlineKeyboardButton("لغو",callback_data="cagame"))
    bot.send_message(cid,f"""
لینک مستقیم ورود به اتاق : {start_game[cid]["url"]}
شماره اتاق : {start_game[cid]["room_num"]}
رمز اتاق : {start_game[cid]["room_pass"]}
""",reply_markup=markup)
    userStep[cid]=0
    

def check_and_notify_thread():
    while True:
        if len(game_info_in_group)>0:
            for gid in game_info_in_group:
                try:
                    time_send=jdatetime.datetime.strptime(game_info_in_group[gid]["time"], "%H:%M %Y/%m/%d")-datetime.timedelta(minutes=15)
                    ir_tz = pytz.timezone('Asia/Tehran')
                    if jdatetime.datetime.strftime(time_send,"%H:%M %Y/%m/%d")==jdatetime.datetime.strftime(jdatetime.datetime.now(ir_tz),"%H:%M %Y/%m/%d"):
                        if len(mid_game_in_group[gid])>0:
                            for number in mid_game_in_group[gid]:
                                try:
                                    bot.send_message(int(mid_game_in_group[gid][number][0]),"بازیکن گرامی برای ثبت حضور خود در بازی وارد گروه شوید و حضور خود را ثبت کنید")
                                except:
                                    pass
                                   
                        else:
                            pass
                except:
                    pass
            for gid in game_info_in_group:
                # try:
                time_send=jdatetime.datetime.strptime(game_info_in_group[gid]["time"], "%H:%M %Y/%m/%d")-datetime.timedelta(minutes=10)
                ir_tz = pytz.timezone('Asia/Tehran')
                if jdatetime.datetime.strftime(time_send,"%H:%M %Y/%m/%d")==jdatetime.datetime.strftime(jdatetime.datetime.now(ir_tz),"%H:%M %Y/%m/%d"):
                    if len(mid_game_in_group[gid])>0:
                        update1=False
                        save_num_removr=[]
                        for number in mid_game_in_group[gid]:
                            # try:
                            if int(mid_game_in_group[gid][number][0]) not in present_dict[gid]:
                                # mid_game_in_group[gid].pop(number)
                                save_num_removr.append(number)
                                # mid=mid_game_in_group[gid][number][2]
                                update1=True
                            # except:
                            #     print("nashod",mid_game_in_group[gid][number][0])
                        if update1:
                            for num in save_num_removr:
                                mid_game_in_group[gid].pop(num)
                        if update1:
                            text=""
                            total_number_reserv=[]
                            for i in mid_game_in_group[gid]:
                                total_number_reserv.append(i)
                                name=mid_game_in_group[gid][i][1]
                                if mid_game_in_group[gid][i][0] in present_dict[gid]:
                                    text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
                                else:
                                    text+=str(i)+"."+str(name)+"\n"
                            markup=InlineKeyboardMarkup()
                            markup_button=[]
                            for i in range(1,int(game_info_in_group[gid]["number"])+1):
                                if i in total_number_reserv:
                                    markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_{i}_ok"))
                                else:
                                    markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
                            markup.add(*markup_button)
                            markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
                            # markup.add(InlineKeyboardButton("🔄تغییر سناریو",url=f"https://t.me/{bot.get_me().username}?start=senario_{gid}_{game_info_in_group[gid]["mid"]}"),InlineKeyboardButton("🔄تغییر ناظر",url=f"https://t.me/{bot.get_me().username}?start=nazer_{gid}_{game_info_in_group[gid]["mid"]}"))
                            markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_senario_{gid}_{game_info_in_group[gid]['mid']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_nazer_{gid}_{game_info_in_group[gid]['mid']}"))
                            markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
                            markup.add(InlineKeyboardButton("❌حذف بازیکن",callback_data="deluser"))
                            bot.edit_message_caption(
f"""
📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
🕰ساعت شروع:{game_info_in_group[gid]["time"]}
👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
{text}
~~~~~~~~~~~~~~~~~~
""",gid,game_info_in_group[gid]["mid"],parse_mode="HTML",reply_markup=markup
            )
                    else:
                        pass
                # except:
                #     print("vddddddddddddddnsssss")
                #     pass
            delete_dict_eleman=False
            list_delete_eleman_dict=[]
#             for gid in game_info_in_group:
#                 try:
#                     time_send=jdatetime.datetime.strptime(game_info_in_group[gid]["time"], "%H:%M %Y/%m/%d")
#                     ir_tz = pytz.timezone('Asia/Tehran')
#                     if jdatetime.datetime.strftime(time_send,"%H:%M %Y/%m/%d")==jdatetime.datetime.strftime(jdatetime.datetime.now(ir_tz),"%H:%M %Y/%m/%d"):
#                         if gid in mid_game_in_group:
#                             if len(mid_game_in_group[gid])>0:
#                                 group_name = game_info_in_group[gid]["name"]
#                                 # new_group = bot.create_chat(title=group_name, type='supergroup')
#                                 # bot.create_chat_invite_link(cid,"mahdi")
#                                 for i in mid_game_in_group[gid]:
#                                     bot.send_message(mid_game_in_group[gid][i][0],f"لینک ورود به بازی برای شروع بازی روی لینک زیر بزنید \n{game_info_in_group[gid]["link_srart_game"]}")

#                                 total_number_reserv=[] 
#                                 # all_cid_reserv=all_cid_reserv.pop(cid)
#                                 # mid_game_in_group[gid].pop(int(all_cid_reserv))
#                                 text=""
#                                 for i in mid_game_in_group[gid]:
#                                     total_number_reserv.append(i)
#                                     name=mid_game_in_group[gid][i][1]
#                                     if mid_game_in_group[gid][i][0] in present_dict[gid]:
#                                         text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
#                                     else:
#                                         text+=str(i)+"."+str(name)+"\n"

#                                 bot.edit_message_caption(
# f"""
# 📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
# 🕰ساعت شروع:{game_info_in_group[gid]["time"]}
# 👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
# 🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
# 👤کسانی که جوین شدند:
# ~~~~~~~~~~~~~~~~~~
# {text}
# ~~~~~~~~~~~~~~~~~~
# بازی در حال اجرا
# """,gid,game_info_in_group[gid]["mid"],parse_mode="HTML"
#                             )
#                                 list_delete_eleman_dict.append(gid)
#                                 delete_dict_eleman=True
#                                 # mid_game_in_group.pop(gid)
#                                 # game_info_in_group.pop(gid)
#                                 # present_dict.pop(gid)

#                             else:
#                                 text=""
#                                 bot.edit_message_caption(
# f"""
# 📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
# 🕰ساعت شروع:{game_info_in_group[gid]["time"]}
# 👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
# 🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
# 👤کسانی که جوین شدند:
# ~~~~~~~~~~~~~~~~~~
# {text}
# ~~~~~~~~~~~~~~~~~~
# بازی به دلیل عدم حضور بازیکن لغو شد
# """,gid,game_info_in_group[gid]["mid"],parse_mode="HTML"
#                             )
#                                 list_delete_eleman_dict.append(gid)
#                                 delete_dict_eleman=True
#                                 # mid_game_in_group.pop(gid)
#                                 # game_info_in_group.pop(gid)
#                                 # present_dict.pop(gid)          
#                         else:
#                             text=""
#                             bot.edit_message_caption(
# f"""
# 📜سناریو:  <a href='{game_info_in_group[gid]["link_info"]}'>{game_info_in_group[gid]["name"]}</a>
# 🕰ساعت شروع:{game_info_in_group[gid]["time"]}
# 👥نام گروه :{game_info_in_group[gid]["gruop_name"]}
# 🎩ناظر: <a href='https://t.me/{game_info_in_group[gid]["nazer"].replace("@","")}'>{game_info_in_group[gid]["name_nazer"]}</a>
# 👤کسانی که جوین شدند:
# ~~~~~~~~~~~~~~~~~~
# {text}
# ~~~~~~~~~~~~~~~~~~
# بازی به دلیل عدم حضور بازیکن لغو شد
# """,gid,game_info_in_group[gid]["mid"],parse_mode="HTML"
#                             )
#                             list_delete_eleman_dict.append(gid)
#                             delete_dict_eleman=True
#                             # mid_game_in_group.pop(gid)
#                             # game_info_in_group.pop(gid)
#                             # present_dict.pop(gid)         

#                 except:
#                     pass
#             if delete_dict_eleman:
#                 for c in list_delete_eleman_dict:
#                     mid_game_in_group.pop(c)
#                     game_info_in_group.pop(c)
#                     present_dict.pop(c)  

        else:
            pass


        threading.Event().wait(56)



check_thread = threading.Thread(target=check_and_notify_thread)
check_thread.start()


bot.infinity_polling()

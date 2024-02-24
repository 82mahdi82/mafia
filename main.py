import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import database
import time
import datetime
import threading
import pytz

database.creat_database_tables()

TOKEN ='6903346134:AAFVD5vdQDRZ5hZ6m1LlBj2C14Y5PeS6HsQ'#'6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'

userStep = {} 
admin=[]#[6926746273]
geam_info={} #cid:{name:...,}
game_info_in_group={}
mid_game_in_group={}#gid:{number:[cid,name,mid]}
present_dict={}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0

# def gen_time_markup():
#     time_now=datetime.datetime.now()
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton(f"ساعت {time_now.hour}", callback_data=f'time_hour_{time_now.hour}'),InlineKeyboardButton(f"دقیقه {time_now.minute}", callback_data='time_minute_{time_now.minute}'))
#     return markup
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
    # print("iiiiiiiiiiiidddddddddd",bot.get_me().id)
    # دریافت اطلاعات عضویت ربات در گروه
    bot_member = bot.get_chat_member(int(chat_id), bot.get_me().id)
    # بررسی اینکه آیا ربات به عنوان ادمین در گروه است یا خیر
    if bot_member.status == 'administrator':
        return True
    else:
        return False
    
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
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
    bot.send_message(m.chat.id,"روند ساخت بازی کنسل شد")
    command_start(m)

@bot.message_handler(content_types=["photo"])
def photo_handler(m):
    cid=m.chat.id
    if get_user_step(cid)==3:
        geam_info[cid].setdefault("photo",m.photo[0].file_id)
        bot.send_message(cid,"لطفا تعداد نفرات شرکت کننده در بازی را مشخص کنید ",reply_markup=gen_number_markup(1))



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
                time_send=datetime.datetime.strptime(game_info_in_group[gid]["time"],"%H:%M")-datetime.timedelta(minutes=15)
                print(time_send)
                ir_tz = pytz.timezone('Asia/Tehran')
                time2 = datetime.datetime.strftime(datetime.datetime.now(ir_tz),"%H:%M")
                time3=datetime.datetime.strptime(time2,"%H:%M")
                if time_send<=time3:
                    present_dict.setdefault(gid,[])
                    if cid not in present_dict[gid]:
                        present_dict[gid].append(cid)
                        bot.answer_callback_query(call.id,"حضور شما ثبت شد")
                        text=""
                        for i in mid_game_in_group[gid]:
                            name=mid_game_in_group[gid][i][1]
                            text+=str(i)+"."+str(name)+"(حاضر)"+"\n"
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
""",gid,mid,parse_mode="HTML"
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("seting"))
def select_chanel(call):
    cid= call.message.chat.id
    data=call.data.split("_")[1]
    mid=call.message.message_id
    tuple_game=database.use_games()[int(data)]
    geam_info.setdefault(cid,{})
    geam_info[cid]={"name":tuple_game[0],"photo":tuple_game[2],"number":tuple_game[3],"link_info":tuple_game[1],"time":tuple_game[4],"gruop_id":tuple_game[5],"gruop_name":tuple_game[6],"nazer":tuple_game[7],"name_nazer":tuple_game[8]}
    select_chanel_and_check(call)
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def select_chanel(call):
    cid= call.message.chat.id
    data=call.data.split("_")[1]
    mid=call.message.message_id
    tuple_game=database.use_games()[int(data)]
    database.delete_games(tuple_game[1])
    bot.delete_message(cid,mid)
    bot.answer_callback_query(call.id,"بازی حذف شد")
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("list"))
def select_chanel(call):
    cid= call.message.chat.id
    list_game=database.use_games()
    if len(list_game)>0:
        total_num=0
        for i in list_game:
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("حذف",callback_data=f"delete_{total_num}"))
            markup.add(InlineKeyboardButton("تنظیمات",callback_data=f"seting_{total_num}_0"))
            bot.send_photo(cid,i[2],f"""
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
                text+=str(i)+"."+str(name)+"\n"
            markup=InlineKeyboardMarkup()
            # markup_button=[]
            # markup_button1=[]
            # if int(game_info_in_group[gid]["number"])%2==0:
            #     for i in range(1,int(game_info_in_group[gid]["number"])//2+1):
            #         if i in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
            #     for b in range(int(game_info_in_group[gid]["number"])//2+1,int(game_info_in_group[gid]["number"])+1):
            #         if b in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button1.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
            # else:
            #     for i in range(1,int(game_info_in_group[gid]["number"])//2+2):
            #         if i in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
            #     for b in range(int(game_info_in_group[gid]["number"])//2+2,int(game_info_in_group[gid]["number"])+1):
            #         if b in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button1.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
            # markup.add(*markup_button)
            # markup.add(*markup_button1)
            markup_button=[]
            for i in range(1,int(game_info_in_group[gid]["number"])+1):
                if i in total_number_reserv:
                    markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
                else:
                    markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
            markup.add(*markup_button)
            markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
            markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_change_senario_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_change_nazer_{game_info_in_group[gid]['gruop_id']}"))
            markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
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
            bot.answer_callback_query(cid,"شما در بازی رزرو نیستید")
    else:
        bot.answer_callback_query(cid,"شما در بازی رزرو نیستید")

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
            if len(mid_game_in_group[gid])>0:
                group_name = game_info_in_group[gid]["name"]
                # new_group = bot.create_chat(title=group_name, type='supergroup')
                # bot.create_chat_invite_link(cid,"mahdi")
                for i in mid_game_in_group[gid]:
                    bot.send_message(mid_game_in_group[gid][i][0],"لینک ورود به بازی برای شروع بازی روی لینک زیر بزنید")
                
                total_number_reserv=[] 
                all_cid_reserv=all_cid_reserv.pop(cid)
                mid_game_in_group[gid].pop(int(all_cid_reserv))
                text=""
                for i in mid_game_in_group[gid]:
                    total_number_reserv.append(i)
                    name=mid_game_in_group[gid][i][1]
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
بازی در حال اجرا
""",gid,mid,parse_mode="HTML"
                )


                mid_game_in_group.pop(gid)
                game_info_in_group.pop(gid)
                present_dict.pop(gid)
            else:
                bot.answer_callback_query(call.id,"هنوز هیچ شرکت کننده ای برای شروع بازی وجود ندارد")
        else:
            bot.answer_callback_query(call.id,"این قابلیت برای ادمین است")
        



@bot.callback_query_handler(func=lambda call: call.data.startswith("reserv"))
def select_chanel(call):
    gid = call.message.chat.id
    cid=call.from_user.id
    mid=call.message.message_id
    data=call.data.split("_")[-1]
    if data=="ok":
        bot.answer_callback_query(call.id,"این شماره قبلا رزرو شده است")
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
            mid_game_in_group[gid].setdefault(int(data),[cid,list_cid_user[cid],mid])
            text=""
            for i in mid_game_in_group[gid]:
                total_number_reserv.append(i)
                name=mid_game_in_group[gid][i][1]
                text+=str(i)+"."+str(name)+"\n"
            markup=InlineKeyboardMarkup()
            # markup_button=[]
            # markup_button1=[]
            # if int(game_info_in_group[gid]["number"])%2==0:
            #     for i in range(1,int(game_info_in_group[gid]["number"])//2+1):
            #         if i in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
            #     for b in range(int(game_info_in_group[gid]["number"])//2+1,int(game_info_in_group[gid]["number"])+1):
            #         if b in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button1.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
            # else:
            #     for i in range(1,int(game_info_in_group[gid]["number"])//2+2):
            #         if i in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
            #     for b in range(int(game_info_in_group[gid]["number"])//2+2,int(game_info_in_group[gid]["number"])+1):
            #         if b in total_number_reserv:
            #             markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
            #         else:
            #             markup_button1.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))

            # markup.add(*markup_button)
            # markup.add(*markup_button1)
            markup_button=[]
            for i in range(1,int(game_info_in_group[gid]["number"])+1):
                if i in total_number_reserv:
                    markup_button.append(InlineKeyboardButton("✅",callback_data=f"reserve_ok"))
                else:
                    markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
            markup.add(*markup_button)

            markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{game_info_in_group[gid]['gruop_id']}"))
            markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_change_senario_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_change_nazer_{game_info_in_group[gid]['gruop_id']}"))
            markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{game_info_in_group[gid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{game_info_in_group[gid]['gruop_id']}"))
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
        bot.answer_callback_query(call.id,"لطفا با استفاده از دمه ثبت نام وارد ربات شوید و ثیت نام کنید")




@bot.callback_query_handler(func=lambda call: call.data.startswith("login"))
def select_chanel(call):
    cid = call.message.chat.id
    bot.send_message(cid,"لطفا نام کاربری خود را وارد کنید:")
    userStep[cid]=20


@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm"))
def select_chanel(call):
    cid = call.message.chat.id
    markup=InlineKeyboardMarkup()
    # markup_button=[]
    # markup_button1=[]
    # if int(geam_info[cid]["number"])%2==0:
    #     for i in range(1,int(geam_info[cid]["number"])//2+1):
    #         markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
    #     for b in range(int(geam_info[cid]["number"])//2+1,int(geam_info[cid]["number"])+1):
    #         markup_button1.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
    # else:
    #     for i in range(1,int(geam_info[cid]["number"])//2+2):
    #         markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
    #     for b in range(int(geam_info[cid]["number"])//2+2,int(geam_info[cid]["number"])+1):
    #         markup_button1.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
    # markup.add(*markup_button)
    # markup.add(*markup_button1)
    markup_button=[]
    for i in range(1,int(geam_info[cid]["number"])+1):
        markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
    markup.add(*markup_button)
    markup.add(InlineKeyboardButton("👤ثبت نام",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("🔴انصراف",callback_data=f"cancel_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🙋حاضری",callback_data=f"present_{geam_info[cid]['gruop_id']}"))
    markup.add(InlineKeyboardButton("🔄تغییر سناریو",callback_data=f"admin_change_senario_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🔄تغییر ناظر",callback_data=f"admin_change_nazer_{geam_info[cid]['gruop_id']}"))
    markup.add(InlineKeyboardButton("❌لغو بازی",callback_data=f"admin_cancel_{geam_info[cid]['gruop_id']}"),InlineKeyboardButton("🎬شروع بازی",callback_data=f"admin_start_{geam_info[cid]['gruop_id']}"))
    bot.send_photo(geam_info[cid]["gruop_id"],geam_info[cid]["photo"],f"""
📜سناریو:  <a href='{geam_info[cid]["link_info"]}'>{geam_info[cid]["name"]}</a>
🕰ساعت شروع:{geam_info[cid]["time"]}
👥نام گروه :{geam_info[cid]["gruop_name"]}
🎩ناظر: <a href='https://t.me/{geam_info[cid]["nazer"].replace("@","")}'>{geam_info[cid]["name_nazer"]}</a>
👤کسانی که جوین شدند:
~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~
""",parse_mode='HTML',reply_markup=markup)
    userStep[cid]=0
    game_info_in_group.setdefault(int(geam_info[cid]["gruop_id"]),{})
    game_info_in_group[int(geam_info[cid]["gruop_id"])]=geam_info[cid]
    geam_info.pop(cid)
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
        bot.send_message(cid,"تایم شروع بازی را وارد کنید (فرمت 00:00):")
        userStep[cid]=14
    elif data=="group":
        list_dict_grups=database.use_table_admin_group()
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
    list_dict_grups=database.use_table_admin_group()
    print(list_dict_grups)
    grup_ok=False
    if len(list_dict_grups)>0:
        for i in list_dict_grups:
            if is_bot_admin(i[0]):
                markup.add(InlineKeyboardButton(i[1],callback_data=f"select_{i[0]}_{i[1]}"))
                grup_ok=True
    else:
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"ربات شما در گروهی عضو نیست لطفا برای ارسال بازی در گروه ربات را در آن گروه اد کنید و ادمین کنید.\nسپس دکمه سرچ را بزنید",reply_markup=markup)
        userStep[cid]=0
        return
    if grup_ok:
        bot.send_message(cid,"لطفا گروهی که میخواهید بازی در آن ارسال شود را انتخاب کنید:",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"لطفا ربات را در گروه هایی که میخواهید بازی را ارسال کنید ادمین کنید.\nسپس دکمه سرچ را بزنید",reply_markup=markup)
    userStep[cid]=0

@bot.callback_query_handler(func=lambda call: call.data.startswith("adding"))
def adding(call):
    cid = call.message.chat.id
    # try:
    print(geam_info)
    database.insert_games(geam_info[cid]["name"],geam_info[cid]["link_info"],geam_info[cid]["photo"],int(geam_info[cid]["number"]),geam_info[cid]["time"],geam_info[cid]["gruop_id"],geam_info[cid]["gruop_name"],geam_info[cid]["nazer"],geam_info[cid]["name_nazer"])
    bot.answer_callback_query(call.id,"بازی در حافظه ذخیره شذ")
    # except:
    #     bot.answer_callback_query(call.id,"قبلا بازی با این لینک ذخیره کرده اید لطفا برای ثبت بازی جدید با همین لینک بازی قبلی را حذغ کنید")

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
        # markup_button=[]
        # if int(geam_info[cid]["number"])%2==0:
        #     for i in range(1,int(geam_info[cid]["number"])//2+1):
        #         markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
        #     for b in range(int(geam_info[cid]["number"])//2+1,int(geam_info[cid]["number"])+1):
        #         markup_button.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
        # else:
        #     for i in range(1,int(geam_info[cid]["number"])//2+2):
        #         markup_button.append(InlineKeyboardButton(f"{i}",callback_data=f"reserve_{i}"))
        #     for b in range(int(geam_info[cid]["number"])//2+2,int(geam_info[cid]["number"])+1):
        #         markup_button.append(InlineKeyboardButton(f"{b}",callback_data=f"reserve_{b}"))
        # # markup.add(tuple(markup_button))
        # markup.add(InlineKeyboardButton("ثبت نام در ربات",url=f"https://t.me/{bot.get_me().username}?start=login"),InlineKeyboardButton("انصراف",callback_data=f"cancel_{data[-1]}"))
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







# @bot.channel_post_handler(content_types=['new_chat_members'])
# def handle_new_channel_member(message):
#     # Assuming you want to store information about the channel and the member
#     channel_id = message.chat.id
#     member_id = message.new_chat_member.id
#     member_username = message.new_chat_member.username

#     # Here you can store this information in a database or any other storage mechanism
#     # For simplicity, let's just print it for now
#     print(f"New member joined channel {channel_id}: {member_username} ({member_id})")


@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def handle_new_member(m):
    print(m)
    print("pkkkkkkkk")
    group_id = m.chat.id
    cid=m.from_user.id
    print(m.chat.title)
    bot_info=bot.get_me()
    if m.new_chat_members[0].username==bot_info.username:
        try:
            database.insert_group(group_id,m.chat.title)
        except:
            pass
        

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    # bot_member = bot.get_chat_member(chat_id, 6926746273)
    # print("staaaaaaaaaaaaatos",bot_member)
    if len(admin)==0:
        admin.append(cid)
    if cid in admin:
        if cid in geam_info:
            geam_info.pop(cid)
        userStep[cid]=0
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("ساخت بازی جدید",callback_data="creat_geam"))
        markup.add(InlineKeyboardButton("لیست بازی های ذخیره شده",callback_data="list"))
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
            bot.send_message(cid,"ثبت نام شما انجام شده و میتوانید در بازی ها شرکت کنید")
        
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
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("به محض تکمیل لیست",callback_data="complete_list"))
    bot.send_message(cid,"لطفا زمان شروع بازی را مشخص کنید (فرمت 00:00)",reply_markup=markup)
    userStep[cid]=5

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==5)
def creat_geam_3(m):
    cid = m.chat.id
    if get_user_step(cid)==5:
        text=m.text
        geam_info.setdefault(cid,{})
        geam_info[cid].setdefault("time",text)
    markup=InlineKeyboardMarkup()
    list_dict_grups=database.use_table_admin_group()
    print(list_dict_grups)
    grup_ok=False
    if len(list_dict_grups)>0:
        for i in list_dict_grups:
            if is_bot_admin(i[0]):
                markup.add(InlineKeyboardButton(i[1],callback_data=f"select_{i[0]}_{i[1]}"))
                grup_ok=True
    else:
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"ربات شما در گروهی عضو نیست لطفا برای ارسال بازی در گروه ربات را در آن گروه اد کنید و ادمین کنید.\nسپس دکمه سرچ را بزنید",reply_markup=markup)
        userStep[cid]=0
        return
    if grup_ok:
        bot.send_message(cid,"لطفا گروهی که میخواهید بازی در آن ارسال شود را انتخاب کنید:",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("سرچ",callback_data="again"))
        bot.send_message(cid,"لطفا ربات را در گروه هایی که میخواهید بازی را ارسال کنید ادمین کنید.\nسپس دکمه سرچ را بزنید",reply_markup=markup)
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
    text=m.text
    geam_info[cid]["time"]=text
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
    try:
        database.insert_users(int(cid),text)
        bot.send_message(cid,"ثبت نام شما با موفقیت انجام شد شما حالا میتوانید در بازی ها شرکت کنید")
    except:
        bot.send_message(cid,"شما قبلا ثبت نام کرده اید")

def check_and_notify_thread():
    while True:
        if len(game_info_in_group)>0:
            for gid in game_info_in_group:
                try:
                    print(game_info_in_group)
                    print(game_info_in_group[gid])
                    time_send=datetime.datetime.strptime(game_info_in_group[gid]["time"],"%H:%M")-datetime.timedelta(minutes=15)
                    print(time_send)
                    ir_tz = pytz.timezone('Asia/Tehran')
                    if datetime.datetime.strftime(time_send,"%H:%M")==datetime.datetime.strftime(datetime.datetime.now(ir_tz),"%H:%M"):
                        if len(mid_game_in_group[gid])>0:
                            for number in mid_game_in_group[gid]:
                                try:
                                    bot.send_message(int(mid_game_in_group[gid][number][0]),"بازیکن گرامی برای ثبت حضور خود در بازی وارد گروه شوید و حضور خود را ثبت کنید")
                                except:
                                    print("nashod",mid_game_in_group[gid][number][0])
                        else:
                            print("ajib",mid_game_in_group)
                            pass
                except:
                    pass
            for gid in game_info_in_group:
                try:
                    time_send=datetime.datetime.strptime(game_info_in_group[gid]["time"],"%H:%M")-datetime.timedelta(minutes=10)
                    print(time_send)
                    ir_tz = pytz.timezone('Asia/Tehran')
                    if datetime.datetime.strftime(time_send,"%H:%M")==datetime.datetime.strftime(datetime.datetime.now(ir_tz),"%H:%M"):
                        if len(mid_game_in_group[gid])>0:
                            update=False
                            for number in mid_game_in_group[gid]:
                                try:
                                    if int(mid_game_in_group[gid][number][0]) not in present_dict[gid]:
                                        mid_game_in_group[gid].pop(number)
                                        mid=mid_game_in_group[gid][number][2]
                                        update=True 
                                except:
                                    print("nashod",mid_game_in_group[gid][number][0])
                            if update:
                                text=""
                                for i in mid_game_in_group[gid]:
                                    name=mid_game_in_group[gid][i][1]
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
""",gid,mid,parse_mode="HTML"
            )

                        else:
                            print("ajib",mid_game_in_group)
                            pass
                except:
                    pass
        else:
            pass


        threading.Event().wait(56)






check_thread = threading.Thread(target=check_and_notify_thread)
check_thread.start()


bot.infinity_polling()

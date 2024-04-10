import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import database
import random
import datetime
import pytz
import amar

database.create_database()

TOKEN ='6317356905:AAGQ2p8Lo0Kc4mkChTmE7ZbI2p1bzw9cIO8'

userStep ={}
admin=748626808
dict_receive_direct_message={}#cid:"off\on"
dict_receive_chat_request={}#cid:"off\on"
dict_cid_chat_anonymous={}#cid:[anony\bpy\girl(you),anony\bpy\girl(search)]
dict_block={}#cid:[id,..]
people_chatting_anonymous={}#cid:uid/uid:cid
dict_posend_info={}
dict_validity={}
list_admin_block=[]

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m)
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

#-----------------------------------------------------------------------def--------------------------------------------------------------------------

def button_nemu():
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("پروفایل👤")
    markup.add("دوست دختر🙋‍","دوست پسر🙋‍♂")
    markup.add("شوگر مامی🙎‍","شوگر ددی🙎‍")
    markup.add("ازدواج موقت👩‍❤️‍👨","ازدواج دائم💍")
    markup.add("همخونه یابی🏠")
    markup.add("🙎‍♂اتصال به ناشناس🙎‍")
    markup.add("تدریس📖","پارتنر علمی👨‍🎓")
    markup.add("انجام پروژه","تبلیغات📰")
    markup.add("پشتیبانی📬","توضیحات")
    markup.add("دعوت دوستان👥")
    return markup

def main_menu_keyboard_for_profile(cid):
    bot.send_message(cid,"کاربر گرامی برای استفاده از این بخش باید ابتدا با استفاده از منو پایین در قسمت 'پروفایل' تمامی فیلد های اطلاعات را پرکنید.",reply_markup=button_nemu())

def button_inlin_edit_profile(cid):
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("اسم",callback_data=f"edit_name_{cid}"),InlineKeyboardButton("جنسیت",callback_data=f"edit_gender_{cid}"))
    markup.add(InlineKeyboardButton("سن",callback_data=f"edit_age_{cid}"),InlineKeyboardButton("تحصیلات",callback_data=f"edit_education_{cid}"))
    markup.add(InlineKeyboardButton("قد",callback_data=f"edit_height_{cid}"),InlineKeyboardButton("وزن",callback_data=f"edit_weight_{cid}"))
    markup.add(InlineKeyboardButton("شغل",callback_data=f"edit_job_{cid}"),InlineKeyboardButton("درآمد",callback_data=f"edit_income_{cid}"))
    markup.add(InlineKeyboardButton("شهر",callback_data=f"edit_province_{cid}"),InlineKeyboardButton("خانه",callback_data=f"edit_home_{cid}"))
    markup.add(InlineKeyboardButton("ماشین",callback_data=f"edit_car_{cid}"),InlineKeyboardButton("وضعیت تاهل",callback_data=f"edit_matrial_{cid}"))
    markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
    return markup

def text_edit_profile(dict_info_profile):
    return f"""
● نام: {dict_info_profile["name"]}
● جنسیت: {dict_info_profile["gender"]}
● سن: {dict_info_profile["age"]}
● تحصیلات: {dict_info_profile["education"]}
● قد: {dict_info_profile["height"]}
● وزن: {dict_info_profile["weight"]}
● شغل: {dict_info_profile["job"]}
● درآمد: {dict_info_profile["income"]}
● شهر: {dict_info_profile["province"]}
● خانه: {dict_info_profile["home"]}
● ماشین: {dict_info_profile["car"]}
● وضعیت تاهل: {dict_info_profile["matrial"]}
                   
🆔 آیدی:/user_{dict_info_profile["ID"]}
"""

#-------------------------------------------------------callback---------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data.startswith("inventory"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برگشت",callback_data="back_profilem"))
    inventory=database.use_profile_table(cid)[0]["validity"]
    bot.send_message(cid,f"""
موجودی شما: {inventory}
""",reply_markup=markup)
    bot.delete_message(cid,mid)


@bot.callback_query_handler(func=lambda call: call.data.startswith("strchatting"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    ID=database.use_profile_table(cid)[0]["ID"]
    uid=int(data[1])
    if uid in dict_cid_chat_anonymous:
        bot.answer_callback_query(call.id,"کاربر مورد نظر در حال چت کردن است")
    else:
        if uid in people_chatting_anonymous:
            bot.answer_callback_query(call.id,"کاربر مورد نظر در حال چت کردن است")
        else:
            people_chatting_anonymous.setdefault(cid,uid)
            people_chatting_anonymous.setdefault(uid,cid)
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("مشاهده پروفایل مخاطب")
            markup.add("پایان چت")
            bot.send_message(cid,"""
درخواست قبول شد
 به کاربر مورد نظر وصل شدید
سلام کنید
""",reply_markup=markup)
            bot.send_message(uid,f"""
درخواست شما از طرف /user_{ID} قبول شد
 به کاربر مورد نظر وصل شدید
سلام کنید
""",reply_markup=markup)
            bot.delete_message(cid,mid)
            userStep[cid]=100
            userStep[uid]=100
        

@bot.callback_query_handler(func=lambda call: call.data.startswith("cancelchatting"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    ID=database.use_profile_table(cid)[0]["ID"]
    uid=int(data[1])
    bot.delete_message(cid,mid)
    bot.send_message(uid,f"""
درخواست شما از طرف /user_{ID} رد شد
""")
    bot.answer_callback_query(call.id,"درخواست رد شد")

@bot.callback_query_handler(func=lambda call: call.data.startswith("request"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    uid=int(data[2])
    ID=database.use_profile_table(cid)[0]["ID"]
    if data[1]=="chat":
        if dict_receive_chat_request[uid]=="on":
            if ID not in dict_block[uid]:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("قبول کردن",callback_data=f"strchatting_{cid}"),InlineKeyboardButton("رد کردن",callback_data=f"cancelchatting_{cid}"))
                bot.send_message(uid,f"""
پیام جدید
درخواست چت
آیدی کاربر: /user_{ID}
""",reply_markup=markup)
                bot.send_message(cid,"درخواست با موفقیت ارسال شد")
            else:
                bot.answer_callback_query(call.id,"کاربر مورد نظر شما را بلاک کرده است")
        else:
            bot.answer_callback_query(call.id,"کاربر مورد نظر چت خود را بسته است")
            
    elif data[1]=="chating":
        bot.answer_callback_query(call.id,"کاربر مورد نظر در حال چت کردن است")
    


@bot.callback_query_handler(func=lambda call: call.data.startswith("blist"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    if cid in dict_block:
        if len(dict_block[cid])>0:
            text=""
            number=1
            for i in dict_block[cid]:
                text+=f"""
{number}.            
مشاهده: /user_{i}
➖➖➖➖➖➖➖➖➖
"""
                number+=1
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برگشت به پروفایل",callback_data="back_profilem"))
                bot.send_message(cid,text,reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,"هیچ کاربری بلاک نشده است")
    else:
        bot.answer_callback_query(call.id,"هیچ کاربری بلاک نشده است")

@bot.callback_query_handler(func=lambda call: call.data.startswith("unblock"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    uid=int(data[1])
    ID=int(data[2])
    dict_block[cid].remove(ID)
    markup=InlineKeyboardMarkup()
    if int(uid) in people_chatting_anonymous:
        markup.add(InlineKeyboardButton("درخواست چت(کاربر درحال چت است)",callback_data=f"request_chating_{uid}_{ID}"))
    else:
        if int(uid) in dict_cid_chat_anonymous:
            markup.add(InlineKeyboardButton("درخواست چت(کاربر درحال چت است)",callback_data=f"request_chating_{uid}_{ID}"))
        else:
            markup.add(InlineKeyboardButton("درخواست چت",callback_data=f"request_chat_{uid}_{ID}"))
 
    markup.add(InlineKeyboardButton("بلاک کردن",callback_data=f"block_{uid}_{ID}"))
    bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    bot.answer_callback_query(call.id,"کاربر مورد نظر با موفقیت آنبلاک شد")


@bot.callback_query_handler(func=lambda call: call.data.startswith("block"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    uid=int(data[1])
    ID=int(data[2])
    dict_block.setdefault(cid,[])
    dict_block[cid].append(ID)
    markup=InlineKeyboardMarkup()
    if int(uid) in people_chatting_anonymous:
        markup.add(InlineKeyboardButton("درخواست چت(کاربر درحال چت است)",callback_data=f"request_chating_{uid}_{ID}"))
    else:
        if int(uid) in dict_cid_chat_anonymous:
            markup.add(InlineKeyboardButton("درخواست چت(کاربر درحال چت است)",callback_data=f"request_chating_{uid}_{ID}"))
        else:
            markup.add(InlineKeyboardButton("درخواست چت",callback_data=f"request_chat_{uid}_{ID}"))
 
    markup.add(InlineKeyboardButton("آنبلاک کردن",callback_data=f"unblock_{uid}_{ID}"))
    bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    bot.answer_callback_query(call.id,"کاربر مورد نظر با موفقیت بلاک شد")

@bot.callback_query_handler(func=lambda call: call.data.startswith("posend"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    id=database.use_profile_table(cid)[0]["ID"]
    post_name=data[2]
    uid=int(data[1])
    print(dict_receive_direct_message)
    if id not in dict_block[uid]:
        if dict_receive_direct_message[uid]=="on":
            dict_posend_info.setdefault(cid,{})
            dict_posend_info[cid]={"post_name":post_name,"uid":uid}
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("لغو",callback_data=f"back_m{post_name}"))
            if cid in people_chatting_anonymous:
                bot.send_message(cid,"از آنجا که شما در حال چت هستید و قصد جواب به دایرکت را دارید پیام بعدی که ارسال کنید به عنوان جواب برای دایرکت ارسال میشود و در چت ارسال نمیشد و پس از پیام بعدی به روال عادی چت برمیگردد \nپیام خود را ارسال کنید:")
            else:
                bot.send_message(cid,"لطفا پیام خود را ارسال کنید:")
            userStep[cid]=200
        else:
            bot.answer_callback_query(call.id,"کاربر مورد نظر دایرکت خود را بسته است")
    else:
        bot.answer_callback_query(call.id,"کاربر مورد نظر شما را بلاک کرده است")

@bot.callback_query_handler(func=lambda call: call.data.startswith("ansposend"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    id=database.use_profile_table(cid)[0]["ID"]
    post_name=data[2]
    uid=int(data[1])
    if id not in dict_block[uid]:
        if dict_receive_direct_message[uid]=="on":
            dict_posend_info.setdefault(cid,{})
            dict_posend_info[cid]={"post_name":post_name,"uid":uid}
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("لغو",callback_data=f"back_m{post_name}"))
            if cid in people_chatting_anonymous:
                bot.send_message(cid,"از آنجا که شما در حال چت هستید و قصد جواب به دایرکت را دارید پیام بعدی که ارسال کنید به عنوان جواب برای دایرکت ارسال میشود و در چت ارسال نمیشد و پس از پیام بعدی به روال عادی چت برمیگردد \nپیام خود را ارسال کنید:")
            else:
                bot.send_message(cid,"لطفا پیام خود را ارسال کنید:")
            userStep[cid]=201
        else:
            bot.add_callback_query_handler(call.id,"کاربر مورد نظر دایرکت خود را بسته است")
    else:
        bot.answer_callback_query(call.id,"کاربر مورد نظر شما را بلاک کرده است")


@bot.callback_query_handler(func=lambda call: call.data.startswith("page"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    list_post=database.use_post_on_table(data[2])
    ofsent=int(data[3])
    start=(ofsent*5)+1
    end=start+5
    text=""
    for i in list_post[start,end]:
        text+=f"""
شناسه پست: {i["shenase"]}
تارخ بروزرسانی: {i["date"]}

مشاهده پست : /viewp_{i["shenase"]}_{data[2]}
➖➖➖➖➖➖➖➖➖
"""
        markup=InlineKeyboardMarkup()
        if ofsent==0:
            markup.add(InlineKeyboardButton("صفحه بعد",callback_data=f"page_next_{data[2]}_{ofsent+1}"))
        elif len(list_post[start+5,end+5])==0:
            markup.add(InlineKeyboardButton("صفحه قبل",callback_data=f"page_back_{data[2]}_{ofsent-1}"))
        else:
            markup.add(InlineKeyboardButton("صفحه قبل",callback_data=f"page_back_{data[2]}_{ofsent-1}"),InlineKeyboardButton("صفحه بعد",callback_data=f"page_next_{data[2]}_{ofsent+1}"))
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[2]}"))
        bot.edit_message_text(text,cid,mid,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("show"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="list":
        list_post=database.use_post_on_table(data[2])
        if len(list_post)>0:
            if len(list_post)>5:
                text=""
                for i in list_post[:6]:
                    text+=f"""
شناسه پست: {i["shenase"]}
تارخ بروزرسانی: {i["date"]}

مشاهده پست : /viewp_{i["shenase"]}_{data[2]}
➖➖➖➖➖➖➖➖➖
"""
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("صفحه بعد",callback_data=f"page_next_{data[2]}_1"))
                markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[2]}"))
                bot.edit_message_text(text,cid,mid,reply_markup=markup)
            else:
                text=""
                for i in list_post:
                    text+=f"""
شناسه پست: {i["shenase"]}
تارخ بروزرسانی: {i["date"]}

مشاهده پست : /viewp_{i["shenase"]}_{data[2]}
➖➖➖➖➖➖➖➖➖
"""
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[2]}"))
                bot.edit_message_text(text,cid,mid,reply_markup=markup)
        else:
            bot.answer_callback_query(call.id,"هنوز پستی ثبت نشده")



@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    database.update_post_one_table(data[1],cid,"post","no")
    bot.answer_callback_query(call.id,"پست شما حذف شد")


@bot.callback_query_handler(func=lambda call: call.data.startswith("receive"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="direct":
        if dict_receive_direct_message[cid]=="off":
            dict_receive_direct_message[cid]="on"
        else:
            dict_receive_direct_message[cid]="off"
    elif data[1]=="chat":
        if dict_receive_chat_request[cid]=="off":
            dict_receive_chat_request[cid]="on"
        else:
            dict_receive_chat_request[cid]="off"

    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("بلاک شده ها",callback_data="blist"),InlineKeyboardButton("موجودی",callback_data="inventory"))
    if dict_receive_direct_message[cid]=="off":
        markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🔴غیر فعال",callback_data=f"receive_direct_message_{cid}"))
    else:
        markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🟢فعال",callback_data=f"receive_direct_message_{cid}"))
    if dict_receive_chat_request[cid]=="off":
        markup.add(InlineKeyboardButton("دریافت درخواست چت: 🔴غیر فعال",callback_data=f"receive_chat_request_{cid}"))
    else:
        markup.add(InlineKeyboardButton("دریافت درخواست چت: 🟢فعال",callback_data=f"receive_chat_request_{cid}"))
    markup.add(InlineKeyboardButton("ویرایش اطلاعات پروفایل",callback_data=f"edit_profile_{cid}"))
    bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
        
@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="profile":
        bot.edit_message_reply_markup(cid,mid,reply_markup=button_inlin_edit_profile(cid))

    elif data[1]=="profilem":
        userStep[cid]=0
        bot.delete_message(cid,mid)
        list_dict_profile_new=database.use_profile_table(cid)
        dict_info_profile=list_dict_profile_new[0]
        print(dict_info_profile)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بلاک شده ها",callback_data="blist"),InlineKeyboardButton("موجودی",callback_data="inventory"))
        if dict_receive_direct_message[cid]=="off":
            markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🔴غیر فعال",callback_data=f"receive_direct_message_{cid}"))
        else:
            markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🟢فعال",callback_data=f"receive_direct_message_{cid}"))
        if dict_receive_chat_request[cid]=="off":
            markup.add(InlineKeyboardButton("دریافت درخواست چت: 🔴غیر فعال",callback_data=f"receive_chat_request_{cid}"))
        else:
            markup.add(InlineKeyboardButton("دریافت درخواست چت: 🟢فعال",callback_data=f"receive_chat_request_{cid}"))
        markup.add(InlineKeyboardButton("ویرایش اطلاعات پروفایل",callback_data=f"edit_profile_{cid}"))
        bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=markup)
        
    elif data[1]=="mprofile":
        bot.delete_message(cid,mid)
        bot.send_message(cid,f"""
منو اصلی
""",reply_markup=button_nemu())
    
    elif data[1]=="girlfriend":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_girlfriend_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_girlfriend_eboutgirl"))
        markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_girlfriend_age"))
        if database.use_post_one_table("girlfriend","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_mgirlfriend"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_girlfriend"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mgirlfriend"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
        

#     elif data[1]=="mgirlfriend":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_girlfriend"))
#         if database.use_post_one_table("girlfriend","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_girlfriend"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_girlfriend"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)
    

    elif data[1]=="boyfriend":
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table("boyfriend",cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table("boyfriend",cid)
        dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_boyfriend_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_boyfriend_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_boyfriend_age"))
        if database.use_post_one_table("boyfriend","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_mboyfriend"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_boyfriend"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mboyfriend"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)



#     elif data[1]=="mboyfriend":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_boyfriend"))
#         if database.use_post_one_table("boyfriend","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_boyfriend"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_boyfriend"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)

    elif data[1]=="hhome":
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table("hhome",cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table("hhome",cid)
        dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_hhome_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_hhome_ebouthhome"))
        markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_hhome_ebouthome"))
        if database.use_post_one_table("hhome","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_mhhome"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_hhome"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mhhome"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

#     elif data[1]=="mhhome":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_hhome"))
#         if database.use_post_one_table("hhome","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_hhome"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_hhome"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)
   
    elif data[1]=="sugermommy":
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table("sugermommy",cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table("sugermommy",cid)
        dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugermommy_ebout"))
        markup.add(InlineKeyboardButton("درباره پسری که میخوام",callback_data="selectpost_sugermommy_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی پسری که میخوام",callback_data="selectpost_sugermommy_age"))
        if database.use_post_one_table("sugermommy","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugermommy"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugermommy"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugermommy"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

#     elif data[1]=="msugermommy":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_sugermommy"))
#         if database.use_post_one_table("sugermommy","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_sugermommy"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_sugermommy"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)

    elif data[1]=="sugerdady":
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table("sugerdady",cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table("sugerdady",cid)
        dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugerdady_ebout"))
        markup.add(InlineKeyboardButton("درباره دختری که میخوام",callback_data="selectpost_sugerdady_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی دختری که میخوام",callback_data="selectpost_sugerdady_age"))
        if database.use_post_one_table("sugerdady","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugerdady"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugerdady"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugerdady"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

#     elif data[1]=="msugerdady":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_sugerdady"))
#         if database.use_post_one_table("sugerdady","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_sugerdady"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_sugerdady"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)


    elif data[1]=="tompmarri":
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table("tompmarri",cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table("tompmarri",cid)
        dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
        markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
        markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
        if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_tompmarri"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mtompmarri"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

#     elif data[1]=="mtompmarri":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_tompmarri"))
#         if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_tompmarri"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_tompmarri"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)

    elif data[1]=="marri":
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table("marri",cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table("marri",cid)
        dict_girl_f_cid=database.use_post_table("marri",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_marri_ebout"))
        markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_marri_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_marri_age"))
        if database.use_post_one_table("marri","post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data="back_mmarri"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_marri"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mmarri"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

#     elif data[1]=="mmarri":
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_marri"))
#         if database.use_post_one_table("marri","post",cid)[0]["post"]=="no":
#             markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_marri"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,cid,mid,reply_markup=markup)
#         else:
#             markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_marri"))
#             markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#             bot.edit_message_text("""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,cid,mid,reply_markup=markup)













    elif data[1].startswith("partner"):
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table(data[1],cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table(data[1],cid)
        dict_girl_f_cid=database.use_post_table(data[1],cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[1]}_ebout"))
        markup.add(InlineKeyboardButton("درباره پارتنری که میخوام",callback_data=f"selectpost_{data[1]}_eboutyou"))
        markup.add(InlineKeyboardButton("رنج سنی پارتنرم",callback_data=f"selectpost_{data[1]}_age"))
        if database.use_post_one_table(data[1],"post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[1]}"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره پارتنری که میخوام: {dict_girl_f_cid["ebout_you"]}
● رنج سنی پارتنرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{data[1]}"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_m{data[1]}"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره پارتنری که میخوام: {dict_girl_f_cid["ebout_you"]}
● رنج سنی پارتنرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

    elif data[1].startswith("teach"):
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table(data[1],cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table(data[1],cid)
        dict_girl_f_cid=database.use_post_table(data[1],cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[1]}_ebout"))
        markup.add(InlineKeyboardButton("چیزی که تدریس میکنم",callback_data=f"selectpost_{data[1]}_whatteach"))
        markup.add(InlineKeyboardButton("سابقه تدریس من",callback_data=f"selectpost_{data[1]}_teachexp"))
        markup.add(InlineKeyboardButton("هزینه تدریس من",callback_data=f"selectpost_{data[1]}_cost"))
        if database.use_post_one_table(data[1],"post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[1]}"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● چیزی که تدریس میکنم: {dict_girl_f_cid["whatteach"]}
● سابقه تدریس من: {dict_girl_f_cid["teach_exp"]}
● هزینه تدریس من: {dict_girl_f_cid["cost"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{data[1]}"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_m{data[1]}"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● چیزی که تدریس میکنم: {dict_girl_f_cid["whatteach"]}
● سابقه تدریس من: {dict_girl_f_cid["teach_exp"]}
● هزینه تدریس من: {dict_girl_f_cid["cost"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)



    elif data[1].startswith("project"):
        dict_info_user=database.use_profile_table(cid)[0]
        list_girl_f=database.use_post_table(data[1],cid)
        if len(list_girl_f)==0:
            database.insert_post_first_table(data[1],cid)
        dict_girl_f_cid=database.use_post_table(data[1],cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[1]}_ebout"))
        markup.add(InlineKeyboardButton("تخصص من",callback_data=f"selectpost_{data[1]}_ecpertise"))
        if database.use_post_one_table(data[1],"post",cid)[0]["post"]=="yes":
            markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[1]}"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره تخصص من: {dict_girl_f_cid["ecpertise"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{data[1]}"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_m{data[1]}"))
            bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره تخصص من: {dict_girl_f_cid["ecpertise"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)


    # elif data[1].startswith("mpartner"):
    else:
        post_name=data[1][1:]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data=f"show_list_{post_name}"))
        if database.use_post_one_table(post_name,"post",cid)[0]["post"]=="no":
            markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"insert_post_{post_name}"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
            bot.edit_message_text("""
برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
""",cid,mid,reply_markup=markup)
        else:
            markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data=f"shpost_{post_name}"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
            bot.edit_message_text("""
برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
""",cid,mid,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("record"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="post":
#         if data[2]=="girlfriend":
#             dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("girlfriend","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("girlfriend","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_girlfriend"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_girlfriend"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)

#         elif data[2]=="boyfriend":
#             dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("boyfriend","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("boyfriend","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_boyfriend"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_boyfriend"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)


#         elif data[2]=="hhome":
#             dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("hhome","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("hhome","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_hhome"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_hhome"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)


#         elif data[2]=="sugermommy":
#             dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("sugermommy","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("sugermommy","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_sugermommy"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_sugermommy"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)
                

#         elif data[2]=="sugerdady":
#             dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("sugerdady","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("sugerdady","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_sugerdady"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_sugerdady"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)

#         elif data[2]=="tompmarri":
#             dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("tompmarri","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("tompmarri","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_tompmarri"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_tompmarri"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)

#         elif data[2]=="marri":
#             dict_girl_f_cid=database.use_post_table("marri",cid)[0]
#             list_check=[]
#             for i in dict_girl_f_cid:
#                 list_check.append(dict_girl_f_cid[i])
#             if "وارد نشده" in list_check:
#                 bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
#             else:
#                 number=0
#                 while True:
#                     list_number=database.use_post_one_table("marri","shenase",cid)
#                     number=random.randint(100000,999999)
#                     if number not in list_number:
#                         break
#                 tehran_timezone = pytz.timezone('Asia/Tehran')
#                 time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#                 database.update_post_last_table("marri","yes",number,"باز",time_now,cid)
#                 markup=InlineKeyboardMarkup()
#                 markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_marri"))
#                 markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_marri"))
#                 markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#                 bot.edit_message_text(f"""
# پست با شناسه: {number}

# مشاهده: /viewp_{number}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)
    
        dict_girl_f_cid=database.use_post_table(data[2],cid)[0]
        list_check=[]
        for i in dict_girl_f_cid:
            list_check.append(dict_girl_f_cid[i])
        if "وارد نشده" in list_check:
            bot.answer_callback_query(call.id,"لطفا تمامی فیلد ها را پرکنید.")
        else:
            number=0
            while True:
                list_number=database.use_post_one_table(data[2],"shenase",cid)
                number=random.randint(100000,999999)
                if number not in list_number:
                    break
            tehran_timezone = pytz.timezone('Asia/Tehran')
            time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
            database.update_post_last_table(data[2],"yes",number,"باز",time_now,cid)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("حذف پست",callback_data=f"delete_{data[2]}"))
            markup.add(InlineKeyboardButton("ویرایش پست",callback_data=f"shpost_{data[2]}"))
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
            bot.edit_message_text(f"""
پست با شناسه: {number}

مشاهده: /viewp_{number}_{data[2]}
بروزرسانی: {time_now}
""",cid,mid,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("shpost"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="girlfriend":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_girlfriend_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_girlfriend_eboutgirl"))
        markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_girlfriend_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_girlfriend"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mgirlfriend"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
    
    elif data[1]=="boyfriend":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_boyfriend_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_boyfriend_eboutgirl"))
        markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_boyfriend_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_boyfriend"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mboyfriend"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
        
    elif data[1]=="hhome":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_hhome_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_hhome_eboutgirl"))
        markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_hhome_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_hhome"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mhhome"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup) 
    
    elif data[1]=="sugermommy":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugermommy_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_sugermommy_eboutgirl"))
        markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_sugermommy_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_sugermommy"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugermommy"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup) 

    elif data[1]=="sugerdady":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugerdady_ebout"))
        markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_sugerdady_eboutgirl"))
        markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_sugerdady_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_sugerdady"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugerdady"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup) 

    elif data[1]=="tompmarri":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
        markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
        markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_tompmarri"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",reply_markup=markup)

    elif data[1]=="marri":
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table("marri",cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_marri_ebout"))
        markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_marri_eboutboy"))
        markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_marri_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_marri"))
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",reply_markup=markup)


    elif data[1].startswith("partner"):
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table(data[1],cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[1]}_ebout"))
        markup.add(InlineKeyboardButton("درباره پارتنری که میخوام",callback_data=f"selectpost_{data[1]}_eboutyou"))
        markup.add(InlineKeyboardButton("رنج سنی پارتنرم",callback_data=f"selectpost_{data[1]}_age"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data=f"delete_{data[1]}"))
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[1]}"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره پارتنری که میخوام: {dict_girl_f_cid["ebout_you"]}
● رنج سنی پارتنرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)

    elif data[1].startswith("teach"):
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table(data[1],cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[1]}_ebout"))
        markup.add(InlineKeyboardButton("چیزی که تدریس میکنم",callback_data=f"selectpost_{data[1]}_whatteach"))
        markup.add(InlineKeyboardButton("سابقه تدریس من",callback_data=f"selectpost_{data[1]}_teachexp"))
        markup.add(InlineKeyboardButton("هزینه تدریس من",callback_data=f"selectpost_{data[1]}_cost"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data=f"delete_{data[1]}"))
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[1]}"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● چیزی که تدریس میکنم: {dict_girl_f_cid["whatteach"]}
● سابقه تدریس من: {dict_girl_f_cid["teach_exp"]}
● هزینه تدریس من: {dict_girl_f_cid["cost"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)


    elif data[1].startswith("project"):
        dict_info_user=database.use_profile_table(cid)[0]
        dict_girl_f_cid=database.use_post_table(data[1],cid)[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[1]}_ebout"))
        markup.add(InlineKeyboardButton("تخصص من",callback_data=f"selectpost_{data[1]}_ecpertise"))
        markup.add(InlineKeyboardButton("حذف پست",callback_data=f"delete_{data[1]}"))
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[1]}"))
        bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره تخصص من: {dict_girl_f_cid["ecpertise"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{data[1]}
""",cid,mid,reply_markup=markup)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("edpost"))
# def nmayesh(call):
#     cid = call.message.chat.id
    # if cid in list_admin_block:
    #     bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
    #     return
#     mid = call.message.message_id
#     data = call.data.split("_")
#     if data[2]=="girlfriend":
#         dict_info_post=database.use_post_table("girlfriend",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("girlfriend","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_girlfriend"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_girlfriend"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)
    
#     elif data[2]=="boyfriend":
#         dict_info_post=database.use_post_table("boyfriend",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("boyfriend","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_boyfriend"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_boyfriend"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)
    
#     elif data[2]=="hhome":
#         dict_info_post=database.use_post_table("hhome",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("hhome","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_hhome"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_hhome"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)
    
#     elif data[2]=="sugermommy":
#         dict_info_post=database.use_post_table("sugermommy",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("sugermommy","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_sugermommy"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_sugermommy"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)
    
#     elif data[2]=="sugerdady":
#         dict_info_post=database.use_post_table("sugerdady",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("sugerdady","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_sugerdady"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_sugerdady"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)

#     elif data[2]=="tompmarri":
#         dict_info_post=database.use_post_table("tompmarri",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("tompmarri","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_tompmarri"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_tompmarri"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)

#     elif data[2]=="marri":
#         dict_info_post=database.use_post_table("marri",cid)[0]
#         tehran_timezone = pytz.timezone('Asia/Tehran')
#         time_now=datetime.datetime.now(tehran_timezone).strftime("%Y-%m-%d %H:%M:%S")
#         database.update_post_last_table("marri","yes",dict_info_post['shenase'],"باز",time_now,cid)
#         markup=InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton("حذف پست",callback_data="delete_marri"))
#         markup.add(InlineKeyboardButton("ویرایش پست",callback_data="shpost_marri"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.edit_message_text(f"""
# پست با شناسه: {dict_info_post['shenase']}

# مشاهده: /viewp_{dict_info_post['shenase']}
# بروزرسانی: {time_now}
# """,cid,mid,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("insert"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="post":
        if data[2]=="girlfriend":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            print(list_check)
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                list_girl_f=database.use_post_table("girlfriend",cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table("girlfriend",cid)
                dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_girlfriend_ebout"))
                markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_girlfriend_eboutgirl"))
                markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_girlfriend_age"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_girlfriend"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_mgirlfriend"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
            
        elif data[2]=="boyfriend":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            print(list_check)
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                list_girl_f=database.use_post_table("boyfriend",cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table("boyfriend",cid)
                dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_boyfriend_ebout"))
                markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_boyfriend_eboutboy"))
                markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_boyfriend_age"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_boyfriend"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_mboyfriend"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
        
        elif data[2]=="hhome":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            print(list_check)
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                list_girl_f=database.use_post_table("hhome",cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table("hhome",cid)
                dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_hhome_ebout"))
                markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_hhome_ebouthhome"))
                markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_hhome_ebouthome"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_hhome"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_mhhome"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
        
        elif data[2]=="sugermommy":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            print(list_check)
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                list_girl_f=database.use_post_table("sugermommy",cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table("sugermommy",cid)
                dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugermommy_ebout"))
                markup.add(InlineKeyboardButton("درباره پسری که میخوام",callback_data="selectpost_sugermommy_eboutboy"))
                markup.add(InlineKeyboardButton("رنج سنی پسری که میخوام",callback_data="selectpost_sugermommy_age"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugermommy"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugermommy"))
                bot.edit_message_text(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
                
        elif data[2]=="sugerdady":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            print(list_check)
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                list_girl_f=database.use_post_table("sugerdady",cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table("sugerdady",cid)
                dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugerdady_ebout"))
                markup.add(InlineKeyboardButton("درباره دختری که میخوام",callback_data="selectpost_sugerdady_eboutboy"))
                markup.add(InlineKeyboardButton("رنج سنی دختری که میخوام",callback_data="selectpost_sugerdady_age"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugerdady"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugerdady"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
        
        elif data[2]=="tompmarri":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                list_boy_f=database.use_post_table("tompmarri",cid)
                if len(list_boy_f)==0:
                    database.insert_post_first_table("tompmarri",cid)
                dict_boy_f_cid=database.use_post_table("tompmarri",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
                markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
                markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
                markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_tompmarri"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_boy_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_boy_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_boy_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_boy_f_cid["dowry"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
        
        elif data[2]=="marri":
            dict_info_user=database.use_profile_table(cid)[0]
            list_check=[]
            for i in dict_info_user:
                list_check.append(dict_info_user[i])
            if "وارد نشده" in list_check:
                main_menu_keyboard_for_profile(cid)
            else:
                dict_boy_f_cid=database.use_post_table("marri",cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_marri_ebout"))
                markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_marri_eboutboy"))
                markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_marri_age"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_marri"))
                markup.add(InlineKeyboardButton("برگشت",callback_data="back_mmarri"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_boy_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_boy_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_boy_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)
                





            
        elif data[2].startswith("partner"):
            dict_info_user=database.use_profile_table(cid)[0]
            text=""
            dict_tranlat={"name":"اسم","gender":"جنسیت","age":"سن","education":"تحصیلات"}
            check=False
            for i in ["name","gender","age","education"]:
                if dict_info_user[i]=="وارد نشده":
                    check=True
                    text+=dict_tranlat[i]+": ❌ |"
                else:
                    text+=dict_tranlat[i]+": ✅ |"
            if check:
                bot.delete_message(cid,mid)
                bot.send_message(cid,f"""
لطفا موارد زیر را در قسمت پروفایل خود تکمیل کنید
تکمیل شده: ✅
تکمیل نشده: ❌
{text}
""",reply_markup=button_nemu())
            else:
                list_girl_f=database.use_post_table(data[2],cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table(data[2],cid)
                dict_girl_f_cid=database.use_post_table(data[2],cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[2]}_ebout"))
                markup.add(InlineKeyboardButton("درباره پارتنری که میخوام",callback_data=f"selectpost_{data[2]}_eboutyou"))
                markup.add(InlineKeyboardButton("رنج سنی پارتنرم",callback_data=f"selectpost_{data[2]}_age"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{data[2]}"))
                markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[2]}"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره پارتنری که میخوام: {dict_girl_f_cid["ebout_you"]}
● رنج سنی پارتنرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)


        elif data[2].startswith("teach"):
            dict_info_user=database.use_profile_table(cid)[0]
            text=""
            dict_tranlat={"name":"اسم","gender":"جنسیت","age":"سن","education":"تحصیلات"}
            check=False
            for i in ["name","gender","age","education"]:
                if dict_info_user[i]=="وارد نشده":
                    check=True
                    text+=dict_tranlat[i]+": ❌ |"
                else:
                    text+=dict_tranlat[i]+": ✅ |"
            if check:
                bot.delete_message(cid,mid)
                bot.send_message(cid,f"""
لطفا موارد زیر را در قسمت پروفایل خود تکمیل کنید
تکمیل شده: ✅
تکمیل نشده: ❌
{text}
""",reply_markup=button_nemu())
            else:
                list_girl_f=database.use_post_table(data[2],cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table(data[2],cid)
                dict_girl_f_cid=database.use_post_table(data[2],cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[2]}_ebout"))
                markup.add(InlineKeyboardButton("چیزی که تدریس میکنم",callback_data=f"selectpost_{data[2]}_whatteach"))
                markup.add(InlineKeyboardButton("سابقه تدریس من",callback_data=f"selectpost_{data[2]}_teachexp"))
                markup.add(InlineKeyboardButton("هزینه تدریس من",callback_data=f"selectpost_{data[2]}_cost"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{data[2]}"))
                markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[2]}"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● چیزی که تدریس میکنم: {dict_girl_f_cid["whatteach"]}
● سابقه تدریس من: {dict_girl_f_cid["teach_exp"]}
● هزینه تدریس من: {dict_girl_f_cid["cost"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)


        elif data[2].startswith("project"):
            dict_info_user=database.use_profile_table(cid)[0]
            text=""
            dict_tranlat={"name":"اسم","gender":"جنسیت","age":"سن","education":"تحصیلات"}
            check=False
            for i in ["name","gender","age","education"]:
                if dict_info_user[i]=="وارد نشده":
                    check=True
                    text+=dict_tranlat[i]+": ❌ |"
                else:
                    text+=dict_tranlat[i]+": ✅ |"
            if check:
                bot.delete_message(cid,mid)
                bot.send_message(cid,f"""
لطفا موارد زیر را در قسمت پروفایل خود تکمیل کنید
تکمیل شده: ✅
تکمیل نشده: ❌
{text}
""",reply_markup=button_nemu())
            else:
                list_girl_f=database.use_post_table(data[2],cid)
                if len(list_girl_f)==0:
                    database.insert_post_first_table(data[2],cid)
                dict_girl_f_cid=database.use_post_table(data[2],cid)[0]
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
                markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{data[2]}_ebout"))
                markup.add(InlineKeyboardButton("تخصص من",callback_data=f"selectpost_{data[2]}_ecpertise"))
                markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{data[2]}"))
                markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{data[2]}"))
                bot.edit_message_text(f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره تخصص من: {dict_girl_f_cid["ecpertise"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",cid,mid,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("edit"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    if data[1]=="profile":
        bot.edit_message_reply_markup(cid,mid,reply_markup=button_inlin_edit_profile(cid))
    elif data[1]=="name":
        bot.delete_message(cid,mid)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لغو و بازگشت",callback_data="back_profilem"))
        bot.send_message(cid,"لطفا اسم خود را ارسال کنید:")
        userStep[cid]=1
    elif data[1]=="age":
        markup=InlineKeyboardMarkup(row_width=5)
        list_age=[]
        for i in range(9,100):
            list_age.append(InlineKeyboardButton(f"{i}",callback_data=f"select_age_{i}"))
        markup.add(*list_age)
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
        # bot.delete_message(cid,mid)
        # markup=InlineKeyboardMarkup()
        # markup.add(InlineKeyboardButton("لغو و بازگشت",callback_data="back_profilem"))
        # bot.send_message(cid,"لطفا سن خود را مانند مثال ارسال کنید(مثال:25)")
        # userStep[cid]=2
    elif data[1]=="height":
        markup=InlineKeyboardMarkup(row_width=5)
        list_age=[]
        for i in range(130,210):
            list_age.append(InlineKeyboardButton(f"{i}",callback_data=f"select_height_{i}"))
        markup.add(*list_age)
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
        # bot.delete_message(cid,mid)
        # markup=InlineKeyboardMarkup()
        # markup.add(InlineKeyboardButton("لغو و بازگشت",callback_data="back_profilem"))
        # bot.send_message(cid,"لطفا قد خود را مانند مثال ارسال کنید(مثال:178):")
        # userStep[cid]=3
    elif data[1]=="weight":
        markup=InlineKeyboardMarkup(row_width=5)
        list_age=[]
        for i in range(30,130):
            list_age.append(InlineKeyboardButton(f"{i}",callback_data=f"select_weight_{i}"))
        markup.add(*list_age)
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
        # bot.delete_message(cid,mid)
        # markup=InlineKeyboardMarkup()
        # markup.add(InlineKeyboardButton("لغو و بازگشت",callback_data="back_profilem"))
        # bot.send_message(cid,"لطفا وزن خود را مانند مثال ارسال کنید(مثال:75):")
        # userStep[cid]=4
    elif data[1]=="province":
        bot.delete_message(cid,mid)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لغو و بازگشت",callback_data="back_profilem"))
        bot.send_message(cid,"لطفا اسم شهر محل زندگی خود را ارسال کنید:")
        userStep[cid]=5

    elif data[1]=="gender":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا جنسیت خود را انتخاب کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("مونث",callback_data=f"select_gender_female"),InlineKeyboardButton("مذکر",callback_data=f"select_gender_male"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif data[1]=="education":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا تحصیلات خود را انتخاب کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("فوق دکترا",callback_data=f"select_education_updoctor"),InlineKeyboardButton("دکترا",callback_data=f"select_education_doctor"))
        markup.add(InlineKeyboardButton("فوق لیسانس",callback_data=f"select_education_uplisans"),InlineKeyboardButton("لیسانس",callback_data=f"select_education_lisans"))
        markup.add(InlineKeyboardButton("فوق دیپلم",callback_data=f"select_education_updiplom"),InlineKeyboardButton("دیپلم",callback_data=f"select_education_diplom"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif data[1]=="job":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا شغل خود را انتخاب کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("شغل آزاد",callback_data=f"select_job_free"),InlineKeyboardButton("شغل دولتی",callback_data=f"select_job_state"))
        markup.add(InlineKeyboardButton("دانشجو",callback_data=f"select_job_univers"),InlineKeyboardButton("بیکار",callback_data=f"select_job_unemploy"))
        markup.add(InlineKeyboardButton("دانش آموز",callback_data=f"select_job_student"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif data[1]=="income":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا درآمد خود را انتخاب کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("0 تا 5 میلیون",callback_data=f"select_income_1"),InlineKeyboardButton("5 تا 10 ملیون",callback_data=f"select_income_2"))
        markup.add(InlineKeyboardButton("10 تا 15 میلیون",callback_data=f"select_income_3"),InlineKeyboardButton("15 تا 20 میلون",callback_data=f"select_income_4"))
        markup.add(InlineKeyboardButton("بالاتر از 20 میلیون",callback_data=f"select_income_5"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif data[1]=="home":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا وضعیت داشتن یا نداشتن خانه خود را مشخص کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("دارم",callback_data=f"select_home_yes"),InlineKeyboardButton("ندارم",callback_data=f"select_home_no"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif data[1]=="car":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا وضعیت داشتن یا نداشتن ماشین خود را مشخص کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("دارم",callback_data=f"select_car_yes"),InlineKeyboardButton("ندارم",callback_data=f"select_car_no"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)
    elif data[1]=="matrial":
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لطفا وضعیت تاهل خود را مشخص کنید",callback_data="none"))
        markup.add(InlineKeyboardButton("متاهل",callback_data=f"select_matrial_yes"),InlineKeyboardButton("مجرد",callback_data=f"select_matrial_no"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_profile"))
        bot.edit_message_reply_markup(cid,mid,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("selectpost"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="girlfriend":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_girlfriend"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=11
            bot.delete_message(cid,mid)
        elif data[2]=="eboutgirl":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_girlfriend"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با دوست دختری که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=12
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_girlfriend"))
            bot.send_message(cid,"لطفا سن دوست دختری که میخواهید را ارسال کنید:",reply_markup=markup)
            userStep[cid]=13
            bot.delete_message(cid,mid)

    elif data[1]=="boyfriend":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_boyfriend"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=14
            bot.delete_message(cid,mid)
        elif data[2]=="eboutboy":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_boyfriend"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با دوست پسری که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=15
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_boyfriend"))
            bot.send_message(cid,"لطفا سن دوست پسری که میخواهید را ارسال کنید:",reply_markup=markup)
            userStep[cid]=16
            bot.delete_message(cid,mid)

    elif data[1]=="hhome":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_hhome"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=17
            bot.delete_message(cid,mid)
        elif data[2]=="ebouthhome":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_hhome"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با همخونه ای که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=18
            bot.delete_message(cid,mid)
        elif data[2]=="ebouthome":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_hhome"))
            bot.send_message(cid,"لطفا ویژگی خونه ای که میخواهید/دارید ارسال کنید:",reply_markup=markup)
            userStep[cid]=19
            bot.delete_message(cid,mid)

    elif data[1]=="sugermommy":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_sugermommy"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=20
            bot.delete_message(cid,mid)
        elif data[2]=="eboutboy":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_sugermommy"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با پسری که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=21
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_sugermommy"))
            bot.send_message(cid,"لطفا رنج سنی پسری که میخواهید را ارسال کنید:",reply_markup=markup)
            userStep[cid]=22
            bot.delete_message(cid,mid)

    elif data[1]=="sugerdady":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_sugerdady"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=23
            bot.delete_message(cid,mid)
        elif data[2]=="eboutboy":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_sugerdady"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با دختری که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=24
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_sugerdady"))
            bot.send_message(cid,"لطفا رنج سنی دختری که میخواهید را ارسال کنید:",reply_markup=markup)
            userStep[cid]=25
            bot.delete_message(cid,mid)
    
    elif data[1]=="tompmarri":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_tompmarri"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=26
            bot.delete_message(cid,mid)
        elif data[2]=="eboutboy":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_tompmarri"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با پسر/دختری که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=27
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_tompmarri"))
            bot.send_message(cid,"لطفا رنج سنی پسر/دختری که میخواهید را ارسال کنید:",reply_markup=markup)
            userStep[cid]=28
            bot.delete_message(cid,mid)
        elif data[2]=="dowry":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_tompmarri"))
            bot.send_message(cid,"چقدر مهریه میدم/میخواهم؟",reply_markup=markup)
            userStep[cid]=29
            bot.delete_message(cid,mid)
    elif data[1]=="marri":
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_marri"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            userStep[cid]=30
            bot.delete_message(cid,mid)
        elif data[2]=="eboutboy":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_marri"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با پسر/دختری که میخواهید ارسال کنید:",reply_markup=markup)
            userStep[cid]=31
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="back_marri"))
            bot.send_message(cid,"لطفا رنج سنی پسر/دختری که میخواهید را ارسال کنید:",reply_markup=markup)
            userStep[cid]=32
            bot.delete_message(cid,mid)




    elif data[1].startswith("partner"):
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            if data[2]=="partnerlang":
                userStep[cid]=33
            else:
                userStep[cid]=34
            bot.delete_message(cid,mid)
        elif data[2]=="eboutyou":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با پارتنری که میخواهید ارسال کنید:",reply_markup=markup)
            if data[2]=="partnerlang":
                userStep[cid]=35
            else:
                userStep[cid]=36
            bot.delete_message(cid,mid)
        elif data[2]=="age":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"لطفا رنج سنن پارتنری که میخواهید را ارسال کنید:",reply_markup=markup)
            if data[2]=="partnerlang":
                userStep[cid]=37
            else:
                userStep[cid]=38
            bot.delete_message(cid,mid)

    elif data[1].startswith("teach"):
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            if data[1]=="teachlang":
                userStep[cid]=39
            elif data[1]=="teachkoo":
                userStep[cid]=40
            elif data[1]=="teachuniv":
                userStep[cid]=41
            else:
                userStep[cid]=42
            bot.delete_message(cid,mid)
        elif data[2]=="whatteach":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"چه چیزی تدریس میکنید:",reply_markup=markup)
            if data[1]=="teachlang":
                userStep[cid]=43
            elif data[1]=="teachkoo":
                userStep[cid]=44
            elif data[1]=="teachuniv":
                userStep[cid]=45
            else:
                userStep[cid]=46
            bot.delete_message(cid,mid)
        elif data[2]=="teachexp":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"سابقه تدریس خود را ارسال کنید:",reply_markup=markup)
            if data[1]=="teachlang":
                userStep[cid]=47
            elif data[1]=="teachkoo":
                userStep[cid]=48
            elif data[1]=="teachuniv":
                userStep[cid]=49
            else:
                userStep[cid]=50
            bot.delete_message(cid,mid)
        elif data[2]=="cost":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"هزینه تدریس خود را ارسال کنید:",reply_markup=markup)
            if data[1]=="teachlang":
                userStep[cid]=51
            elif data[1]=="teachkoo":
                userStep[cid]=52
            elif data[1]=="teachuniv":
                userStep[cid]=53
            else:
                userStep[cid]=54
            bot.delete_message(cid,mid)

    elif data[1].startswith("project"):
        if data[2]=="ebout":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با خود ارسال کنید:",reply_markup=markup)
            if data[1]=="projectuinv":
                userStep[cid]=55
            else:
                userStep[cid]=56
            bot.delete_message(cid,mid)
        elif data[2]=="ecpertise":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_{data[1]}"))
            bot.send_message(cid,"لطفا توضیحاتی را در رابطه با تخصص خود ارسال کنید:",reply_markup=markup)
            if data[1]=="projectuinv":
                userStep[cid]=57
            else:
                userStep[cid]=58
            bot.delete_message(cid,mid)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select"))
def nmayesh(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1]=="gender":
        if data[2]=="female":
            database.update_profile_one_table(cid,"gender","مونث")
        elif data[2]=="male":
            database.update_profile_one_table(cid,"gender","مذکر")
    elif data[1]=="education":
        if data[2]=="updoctor":
            database.update_profile_one_table(cid,"education","فوق دکترا")
        elif data[2]=="doctor":
            database.update_profile_one_table(cid,"education","دکترا")
        elif data[2]=="uplisans":
            database.update_profile_one_table(cid,"education","فوق لیسانس")
        elif data[2]=="lisans":
            database.update_profile_one_table(cid,"education","لیسانس")
        elif data[2]=="updiplom": 
            database.update_profile_one_table(cid,"education","فوق دیپلم")
        elif data[2]=="diplom":
            database.update_profile_one_table(cid,"education","دیپلم")
    elif data[1]=="job":
        if data[2]=="free":
            database.update_profile_one_table(cid,"job","آزاد")
        elif data[2]=="state":
            database.update_profile_one_table(cid,"job","کارمند")
        elif data[2]=="univers":
            database.update_profile_one_table(cid,"job","دانشجو")
        elif data[2]=="unemploy":
            database.update_profile_one_table(cid,"job","بیکار")
        elif data[2]=="student":
            database.update_profile_one_table(cid,"job","دانش آموز")
    elif data[1]=="income":
        if data[2]=="1":
            database.update_profile_one_table(cid,"income","0 تا 5 میلیون")
        elif data[2]=="2":
            database.update_profile_one_table(cid,"income","5 تا 10 ملیون")
        elif data[2]=="3":
            database.update_profile_one_table(cid,"income","10 تا 15 میلیون")
        elif data[2]=="4":
            database.update_profile_one_table(cid,"income","15 تا 20 میلون")
        elif data[2]=="5":
            database.update_profile_one_table(cid,"income","بالاتر از 20 میلیون")
    elif data[1]=="home":
        if data[2]=="yes":
            database.update_profile_one_table(cid,"home","دارم")
        elif data[2]=="no":
            database.update_profile_one_table(cid,"home","ندارم")
    elif data[1]=="car":
        if data[2]=="yes":
            database.update_profile_one_table(cid,"car","دارم")
        elif data[2]=="no":
            database.update_profile_one_table(cid,"car","ندارم")
    elif data[1]=="matrial":
        if data[2]=="yes":
            database.update_profile_one_table(cid,"matrial","متاهل")
        elif data[2]=="no":
            database.update_profile_one_table(cid,"matrial","مجرد")
    elif data[1]=="age":
        database.update_profile_one_table(cid,"age",data[2])
    elif data[1]=="height":
        database.update_profile_one_table(cid,"height",data[2])
    elif data[1]=="weight":
        database.update_profile_one_table(cid,"weight",data[2])

    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    print(dict_info_profile)
    # markup=InlineKeyboardMarkup()
    # if dict_receive_direct_message[cid]=="off":
    #     markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🔴غیر فعال",callback_data=f"receive_direct_message_{cid}"))
    # else:
    #     markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🟢فعال",callback_data=f"receive_direct_message_{cid}"))
    # if dict_receive_chat_request[cid]=="off":
    #     markup.add(InlineKeyboardButton("دریافت درخواست چت: 🔴غیر فعال",callback_data=f"receive_chat_request_{cid}"))
    # else:
    #     markup.add(InlineKeyboardButton("دریافت درخواست چت: 🟢فعال",callback_data=f"receive_chat_request_{cid}"))
    # markup.add(InlineKeyboardButton("ویرایش اطلاعات پروفایل",callback_data=f"edit_profile_{cid}"))
    bot.edit_message_caption(text_edit_profile(dict_info_profile),cid,mid,reply_markup=button_inlin_edit_profile(cid))



#----------------------------------------------------------------------admin--------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("panel"))
def call_callback_panel_amar(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")[-1]
    countOfUsers=len(database.use_all_profile())
    if countOfUsers>0:
        if data=="amar":
            countOfUsers=len(database.use_all_profile())
            txt = f'آمار کاربران: {countOfUsers} نفر '
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_text(txt,cid,mid,reply_markup=markup)
        elif data=="brodcast":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_text("برای ارسال همگانی پیام لطفا پیام خود را ارسال کنید و در غیر این صورت برای بازگشت به پنل از دکمه زیر استفاده کنید",cid,mid,reply_markup=markup)
            userStep[cid]=1000
        elif data=="forall":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_text("برای فوروارد همگانی پیام لطفا پیام خود را ارسال کنید و در غیر این صورت برای بازگشت به پنل از دکمه زیر استفاده کنید",cid,mid,reply_markup=markup)
            userStep[cid]=1001
    else:
        bot.answer_callback_query(call.id,"هنوز کاربری وجود ندارد")


@bot.callback_query_handler(func=lambda call: call.data.startswith("admin"))
def call_callback_panel_amar(call):
    cid = call.message.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    mid = call.message.message_id
    data = call.data.split("_")
    if len(data)==2:
        if data[1]=="vailidity":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_text("برای تغییر اعتبار لطفا آیدی کاربر را ارسال کنید:",cid,mid,reply_markup=markup)
            userStep[cid]=1002
        elif data[1]=="Amounts":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("نمودار بر اساس جنسیت کاربران",callback_data="admin_Amounts_gender"))
            markup.add(InlineKeyboardButton("نمودار بر اساس سن کاربران",callback_data="admin_Amounts_age"))
            markup.add(InlineKeyboardButton("نمودار بر اساس شغل کاربران",callback_data="admin_Amounts_job"))
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_text("یکی از گزینه های زیر را انخاب کنید",cid,mid,reply_markup=markup)
    if len(data)==3:
        if data[1]=="back": 
            userStep[cid]=0
            if data[2]=="panel":
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(' تعداد کاربران',callback_data='panel_amar'))
                markup.add(InlineKeyboardButton("آمار نموداری کاربران",callback_data="admin_Amounts"))
                markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='panel_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='panel_forall'))
                markup.add(InlineKeyboardButton("تغییر اعتبار",callback_data="admin_vailidity"))
                bot.edit_message_text("""
پنل مدیریت
برای مشاهده و حذف کاربران آیدی کاربر را ارسال کنید
""",cid,mid,reply_markup=markup)


        elif data[1]=="Amounts":
            if data[2]=="gender":
                list_gender=[]
                list_all_info=database.use_all_profile()
                for i in list_all_info:
                    list_gender.append(i["gender"])
                photo_path=amar.get_Amounts(list_gender)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(cid, photo)
                bot.send_message(cid,"نمودار کاربران براساس جنسیت",reply_markup=markup)

            elif data[2]=="age":
                list_gender=[]
                list_all_info=database.use_all_profile()
                for i in list_all_info:
                    list_gender.append(i["age"])
                photo_path=amar.get_Amounts(list_gender)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(cid, photo)
                bot.send_message(cid,"نمودار کاربران براساس سن",reply_markup=markup)
            elif data[2]=="job": 
                list_gender=[]
                list_all_info=database.use_all_profile()
                for i in list_all_info:
                    list_gender.append(i["job"])
                photo_path=amar.get_Amounts(list_gender)
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(cid, photo)
                bot.send_message(cid,"نمودار کاربران براساس شفل",reply_markup=markup)
            
        elif data[1]=="block":
            uid=int(data[2])
            list_admin_block.append(uid)
            bot.answer_callback_query(call.id,"کاربر مورد نظر بلاک شد")
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("آنبلاک کردن کاربر",callback_data=f"admin_unblock_{uid}"))
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)

        elif data[1]=="unblock":
            uid=int(data[2])
            list_admin_block.remove(uid)
            bot.answer_callback_query(call.id,"کاربر مورد نظر بلاک شد")
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بلاک کردن کاربر",callback_data=f"admin_block_{uid}"))
            markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
            bot.edit_message_reply_markup(cid,mid,reply_markup=markup)

    if len(data)==4:
        if data[1]=="validity":
            if data[2]=="add":
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("لغو و بازگشت به پنل",callback_data="admin_back_panel"))
                bot.send_message(cid,"مقداری که میخواهید اعتبار را افزایش به صورت عددی ارسال کنید:",reply_markup=markup)
                dict_validity.setdefault('ID',0)
                dict_validity["ID"]=int(data[3])
                userStep[cid]=1003
            elif data[2]=="sub":
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("لغو و بازگشت به پنل",callback_data="admin_back_panel"))
                bot.send_message(cid,"مقداری که میخواهید اعتبار را کاهش به صورت عددی ارسال کنید:",reply_markup=markup)
                dict_validity.setdefault('ID',0)
                dict_validity["ID"]=int(data[3])
                userStep[cid]=1004

#-----------------------------------------------------------------commands-----------------------------------------------------------



@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    userStep[cid]=0
    if cid == admin:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(' تعداد کاربران',callback_data='panel_amar'))
        markup.add(InlineKeyboardButton("آمار نموداری کاربران",callback_data="admin_Amounts"))
        markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='panel_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='panel_forall'))
        markup.add(InlineKeyboardButton("تغییر اعتبار",callback_data="admin_vailidity"))
        bot.send_message(cid,"""
سلام ادمین گرامی به ربات خوش آمدید
برای تنظیم ربات از دکمه های زیر استفاده کنید
و برای مشاهده و حذف کاربران آیدی کاربر را ارسال کنید
""",reply_markup=markup)
    else:
        dict_receive_direct_message.setdefault(cid,"on")
        dict_receive_chat_request.setdefault(cid,"on")
        dict_block.setdefault(cid,[])
        list_dict_profile=database.use_profile_table(cid)
        if len(list_dict_profile)==0:
            if len(m.text.split(" "))==2:
                list_id_for_va=database.use_profile_id_table(int(m.text.split(" ")[1]))
                if len(list_id_for_va)==1:
                    uid=int(list_id_for_va[0]["cid"])
                    if cid != uid:
                        database.add_validity(uid,1000)
                        bot.send_message(uid,"یک کاربر با لینک دعوت شما وارد ربات شد و یه موجودی شما هزار تومن اضافه شد")
            list_dict_pr=database.all_use_profile_table()
            if len(list_dict_pr)>0:
                list_id=[]
                for i in list_dict_pr:
                    list_id.append(i["ID"])
                id=0
                print(list_id)
                while True:
                    id=random.randint(1000000,9999999)
                    if id not in list_id:
                        break
                database.insert_profile_first_table(cid,id)
                
            else:
                id=random.randint(1000000,9999999)
                database.insert_profile_first_table(cid,id)

        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        if cid in dict_cid_chat_anonymous:
            markup.add("لغو جستجو")
        markup.add("پروفایل👤")
        markup.add("دوست دختر🙋‍","دوست پسر🙋‍♂")
        markup.add("شوگر مامی🙎‍","شوگر ددی🙎‍")
        markup.add("ازدواج موقت👩‍❤️‍👨","ازدواج دائم💍")
        markup.add("همخونه یابی🏠")
        markup.add("🙎‍♂اتصال به ناشناس🙎‍")
        markup.add("تدریس📖","پارتنر علمی👨‍🎓")
        markup.add("انجام پروژه","تبلیغات📰")
        markup.add("پشتیبانی📬","توضیحات")
        markup.add("دعوت دوستان👥")
        bot.send_message(cid,f"""
سلام {m.chat.first_name} عزیز 
به ربات دوست یابی خوش آمدید برای استفاده از ربات از دکمه های زیر استفاده کنید
""",reply_markup=markup)


#------------------------------------------------------------m.text-----------------------------------------------------------------
        


@bot.message_handler(func=lambda m: m.text.startswith("/user_"))
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text.split("_")
    id=int(text[1])
    list_chheck=database.use_profile_id_table(int(id))
    if len(list_chheck)==1:
        dict_info_user=database.use_profile_id_table(int(id))[0]
        if cid==admin:
            if get_user_step(cid)==1002:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("کاهش اعتبار",callback_data=f"admin_validity_sub_{id}"),InlineKeyboardButton(f"افزایش اعتبار",callback_data=f"admin_validity_add_{id}"))
                markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
                bot.send_message(cid,f"""
اسم کاربر: {dict_info_user["name"]}
موجودی کاربر: {dict_info_user["validity"]} تومن
""",reply_markup=markup)
                return
            else:
                markup=InlineKeyboardMarkup()
                if dict_info_user["cid"] not in list_admin_block:
                    markup.add(InlineKeyboardButton("بلاک کردن کاربر",callback_data=f"admin_block_{dict_info_user["cid"]}"))
                else:
                    markup.add(InlineKeyboardButton("آنبلاک کردن کاربر",callback_data=f"admin_unblock_{dict_info_user["cid"]}"))
                markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
                bot.send_message(cid,text_edit_profile(dict_info_user)+f"\nموجودی: {dict_info_user["validity"]}",reply_markup=markup)
                return
            

        
        dict_info_user=database.use_profile_id_table(int(id))[0]
        if dict_info_user["cid"]!=cid:
            markup=InlineKeyboardMarkup()
            if int(dict_info_user["cid"]) in people_chatting_anonymous:
                markup.add(InlineKeyboardButton("درخواست چت(کاربر درحال چت است)",callback_data=f"request_chating_{dict_info_user["cid"]}_{id}"))
            else:
                if int(dict_info_user["cid"]) in dict_cid_chat_anonymous:
                    markup.add(InlineKeyboardButton("درخواست چت(کاربر درحال چت است)",callback_data=f"request_chating_{dict_info_user["cid"]}_{id}"))
                else:
                    markup.add(InlineKeyboardButton("درخواست چت",callback_data=f"request_chat_{dict_info_user["cid"]}_{id}"))
            if cid in dict_block:
                if id in dict_block[cid]:
                    markup.add(InlineKeyboardButton("آنبلاک کردن",callback_data=f"unblock_{dict_info_user["cid"]}_{id}"))
                else:
                    markup.add(InlineKeyboardButton("بلاک کردن",callback_data=f"block_{dict_info_user["cid"]}_{id}"))
            else:
                markup.add(InlineKeyboardButton("بلاک کردن",callback_data=f"block_{dict_info_user["cid"]}_{id}"))
            # markup.add(InlineKeyboardButton("ارسال پیام",callback_data=f"send_m_{dict_info_user["cid"]}"))
            print(dict_info_user)
            bot.send_photo(cid,dict_info_user["photo"],text_edit_profile(dict_info_user),reply_markup=markup)
        else:
            def_show_profile(m)
    else:
        bot.send_message(cid,"آیدی ارسال شده وجود ندارد")


@bot.message_handler(func=lambda m: m.text.startswith("/viewp_"))
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text.split("_")
    shenase=text[1]
    post_name=text[2]
    list_info=database.use_post_table_shenase(post_name,shenase)
    if len(list_info)>0:
        dict_info=list_info[0]
        dict_profile=database.use_profile_table(dict_info["cid"])[0]
        if post_name=="girlfriend":
            text=f"""
موضوع پست: دوست دختر
● درباره من: {dict_info["ebout"]}
● درباره دوست دختری که میخوام: {dict_info["ebout_girl"]}
● رنج سنی دوست دختری که میخوام: {dict_info["age_f"]}
"""
        elif post_name=="boyfriend":
            text=f"""
موضوع پست: دوست پسر
● درباره من: {dict_info["ebout"]}
● درباره دوست پسری که میخوام: {dict_info["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_info["age_f"]}
"""
        elif post_name=="hhome":
            text=f"""
موضوع پست: همخونه
● درباره من: {dict_info["ebout"]}
● درباره همخونه ای که میخوام: {dict_info["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_info["ebout_home"]}
"""
        elif post_name=="sugermommy":
            text=f"""
موضوع پست: شوگرمامی
● درباره من: {dict_info["ebout"]}
● درباره پسری که میخوام: {dict_info["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_info["age_f"]}
"""
        elif post_name=="sugerdady":
            text=f"""
موضوع پست: شوگرددی
● درباره من: {dict_info["ebout"]}
● درباره دختری که میخوام: {dict_info["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_info["age_f"]}
"""
        elif post_name=="tompmarri":
            text=f"""
موضوع پست: ازدواج موقت
● درباره من: {dict_info["ebout"]}
● درباره پسر/دختری که میخوام: {dict_info["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_info["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_info["dowry"]}
"""
        elif post_name=="marri":
            text=f"""
موضوع پست: ازدواج دائم
● درباره من: {dict_info["ebout"]}
● درباره پسر/دختری که میخوام: {dict_info["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_info["age_f"]}
"""
        elif post_name=="partnerlang":
            text=f"""
موضوع پست: پارتنر زبان
● درباره هدف من: {dict_info["ebout"]}
● درباره پارتنری که میخوام: {dict_info["ebout_you"]}
● رنج سنی پارتنرم: {dict_info["age_f"]}
"""
        elif post_name=="partnerkoo":
            text=f"""
موضوع پست: پارتنر کنکور
● درباره هدف من: {dict_info["ebout"]}
● درباره پارتنری که میخوام: {dict_info["ebout_you"]}
● رنج سنی پارتنرم: {dict_info["age_f"]}
"""
        elif post_name=="teachlang":
            text=f"""
موضوع پست: تدریس زبان
● درباره من: {dict_info["ebout"]}
● چیزی که تدریس میکنم: {dict_info["whatteach"]}
● سابقه تدریس من: {dict_info["teach_exp"]}
● هزینه تدریس من: {dict_info["cost"]}
"""
        elif post_name=="teachkoo":
            text=f"""
موضوع پست: تدریس دروس کنکور
● درباره هدف من: {dict_info["ebout"]}
● چیزی که تدریس میکنم: {dict_info["whatteach"]}
● سابقه تدریس من: {dict_info["teach_exp"]}
● هزینه تدریس من: {dict_info["cost"]}
"""
        elif post_name=="teachuniv":
            text=f"""
موضوع پست: تدریس دروس دانشگاهی
● درباره هدف من: {dict_info["ebout"]}
● چیزی که تدریس میکنم: {dict_info["whatteach"]}
● سابقه تدریس من: {dict_info["teach_exp"]}
● هزینه تدریس من: {dict_info["cost"]}
"""
        elif post_name=="teachsys":
            text=f"""
موضوع پست: تدریس نرم افزار
● درباره هدف من: {dict_info["ebout"]}
● چیزی که تدریس میکنم: {dict_info["whatteach"]}
● سابقه تدریس من: {dict_info["teach_exp"]}
● هزینه تدریس من: {dict_info["cost"]}
"""
        elif post_name=="projectuinv":
            text=f"""
موضوع پست: انجام پروژه درسی
● درباره هدف من: {dict_info["ebout"]}
● درباره تخصص من: {dict_info["ecpertise"]}
"""
        elif post_name=="projectwork":
            text=f"""
موضوع پست: انجام پروژه حرفه ای
● درباره هدف من: {dict_info["ebout"]}
● درباره تخصص من: {dict_info["ecpertise"]}
"""


        markup=InlineKeyboardMarkup()
        if dict_info["cid"]==cid:
            markup.add(InlineKeyboardButton("ویرایش پست",callback_data=f"shpost_{post_name}"),InlineKeyboardButton("برگشت به لیست",callback_data=f"show_list_{post_name}"))
        else:
            markup.add(InlineKeyboardButton("ارسال پیام",callback_data=f"posend_{dict_info["cid"]}_{post_name}"),InlineKeyboardButton("برگشت به لیست",callback_data=f"show_list_{post_name}"))#posend_cidpost_postname
        bot.send_message(cid,f"""
شناسه پست: {dict_info["shenase"]}

{text}
                         
پروفایل پست گذار: /user_{dict_profile["ID"]}
بروزرسانی : {dict_info["date"]}
""",reply_markup=markup)
    else:
        bot.send_message(cid,"پستی با این مشخصات وجود ندارد")
        userStep[cid]=0

@bot.message_handler(func=lambda m: m.text=="منو اصلی📜")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    userStep[cid]=0
    text=m.text
    bot.send_message(cid,text,reply_markup=button_nemu())
@bot.message_handler(func=lambda m: m.text=="پروفایل👤")
def def_show_profile(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    userStep[cid]=0
    dict_receive_direct_message.setdefault(cid,"on")
    dict_receive_chat_request.setdefault(cid,"on")
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    print(dict_info_profile)
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("بلاک شده ها",callback_data="blist"),InlineKeyboardButton("موجودی",callback_data="inventory"))
    if dict_receive_direct_message[cid]=="off":
        markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🔴غیر فعال",callback_data=f"receive_direct_message_{cid}"))
    else:
        markup.add(InlineKeyboardButton("دریافت پیام دایرکت: 🟢فعال",callback_data=f"receive_direct_message_{cid}"))
    if dict_receive_chat_request[cid]=="off":
        markup.add(InlineKeyboardButton("دریافت درخواست چت: 🔴غیر فعال",callback_data=f"receive_chat_request_{cid}"))
    else:
        markup.add(InlineKeyboardButton("دریافت درخواست چت: 🟢فعال",callback_data=f"receive_chat_request_{cid}"))
    markup.add(InlineKeyboardButton("ویرایش اطلاعات پروفایل",callback_data=f"edit_profile_{cid}"))
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=markup)



@bot.message_handler(func=lambda m: m.text=="زبان" or m.text=="کنکور" or m.text=="دروس کنکور" or m.text=="دروس دانشگاهی"
                       or m.text=="زبان🖋" or m.text=="نرم افزار💻" or m.text=="درسی و دانشگاهی" or m.text=="حرفه ای" or m.text=="دوست دختر🙋‍"
                       or m.text=="دوست پسر🙋‍♂" or m.text=="همخونه یابی🏠" or m.text=="شوگر مامی🙎‍" or m.text=="شوگر ددی🙎‍"
                       or m.text=="ازدواج موقت👩‍❤️‍👨" or m.text=="ازدواج دائم💍")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    userStep[cid]=0
    if m.text=="دوست دختر🙋‍":
        post_name="girlfriend"
    elif m.text=="دوست پسر🙋‍♂":
        post_name="boyfriend"
    elif m.text=="دوست پسر🙋‍♂":
        post_name="boyfriend"
    elif m.text=="همخونه یابی🏠":
        post_name="hhome"
    elif m.text=="شوگر مامی🙎‍":
        post_name="sugermommy"
    elif m.text=="شوگر ددی🙎‍":
        post_name="sugerdady"
    elif m.text=="ازدواج موقت👩‍❤️‍👨":
        post_name="tompmarri"
    elif m.text=="ازدواج دائم💍":
        post_name="marri"

    elif m.text=="زبان" :
        post_name="partnerlang"
    elif m.text=="کنکور":
        post_name="partnerkoo"

    elif m.text=="زبان🖋":
        post_name="teachlang" 
    elif m.text=="نرم افزار💻":
        post_name="teachsys" 
    elif m.text=="دروس کنکور":
        post_name="teachkoo" 
    elif m.text=="دروس دانشگاهی":
        post_name="teachuniv" 

    elif m.text=="درسی و دانشگاهی":
        post_name="projectuinv" 
    elif m.text=="حرفه ای":
        post_name="projectwork" 
    check=database.use_post_table(post_name,cid)
    if len(check)==0:
        database.insert_post_first_table(post_name,cid)
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data=f"show_list_{post_name}"))
    if database.use_post_one_table(post_name,"post",cid)[0]["post"]=="no":
        markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"insert_post_{post_name}"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
        bot.send_message(cid,"""
برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data=f"shpost_{post_name}"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
        bot.send_message(cid,"""
برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
""",reply_markup=markup)

# @bot.message_handler(func=lambda m: m.text=="دوست دختر🙋‍")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("girlfriend",cid)
#     if len(check)==0:
#         database.insert_post_first_table("girlfriend",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_girlfriend"))
#     if database.use_post_one_table("girlfriend","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_girlfriend"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_girlfriend"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)
    


# @bot.message_handler(func=lambda m: m.text=="دوست پسر🙋‍♂")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("boyfriend",cid)
#     if len(check)==0:
#         database.insert_post_first_table("boyfriend",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_boyfriend"))
#     if database.use_post_one_table("boyfriend","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_boyfriend"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_boyfriend"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)
    


# @bot.message_handler(func=lambda m: m.text=="همخونه یابی🏠")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("hhome",cid)
#     if len(check)==0:
#         database.insert_post_first_table("hhome",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_hhome"))
#     if database.use_post_one_table("hhome","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_hhome"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_hhome"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)


# @bot.message_handler(func=lambda m: m.text=="شوگر مامی🙎‍")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("sugermommy",cid)
#     if len(check)==0:
#         database.insert_post_first_table("sugermommy",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_sugermommy"))
#     if database.use_post_one_table("sugermommy","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_sugermommy"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_sugermommy"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)


# @bot.message_handler(func=lambda m: m.text=="شوگر ددی🙎‍")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("sugerdady",cid)
#     if len(check)==0:
#         database.insert_post_first_table("sugerdady",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_sugerdady"))
#     if database.use_post_one_table("sugerdady","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_sugerdady"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_sugerdady"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)



# @bot.message_handler(func=lambda m: m.text=="ازدواج موقت👩‍❤️‍👨")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("tompmarri",cid)
#     if len(check)==0:
#         database.insert_post_first_table("tompmarri",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_tompmarri"))
#     if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_tompmarri"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_tompmarri"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)


# @bot.message_handler(func=lambda m: m.text=="ازدواج دائم💍")
# def handel_text(m):
#     cid=m.chat.id
#     text=m.text
#     mid=m.message_id
#     userStep[cid]=0
#     check=database.use_post_table("marri",cid)
#     if len(check)==0:
#         database.insert_post_first_table("marri",cid)
#     markup=InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("مشاهده پست های قبلی",callback_data="show_list_marri"))
#     if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="no":
#         markup.add(InlineKeyboardButton("ثبت پست",callback_data="insert_post_marri"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای ثبت پست خود در این بخش از دکمه 'ثبت پست' استفاده کنید
# """,reply_markup=markup)
#     else:
#         markup.add(InlineKeyboardButton("مشاهده پست ثبت شده",callback_data="shpost_marri"))
#         markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mprofile"))
#         bot.send_message(cid,"""
# برای مشاهده پست های قبلی ثبت شده در این بخش از دکمه 'مشاهده پشت های قبلی' استفاده کنید
# و برای مشاهده پست ثبت شده خود در این بخش از دکمه 'مشاهده پست ثبت شده' استفاده کنید
# """,reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="🙎‍♂اتصال به ناشناس🙎‍")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    userStep[cid]=0
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲جستجو شانسی🎲")
    markup.add("🙋‍♂جستجو پسر🙋‍♂","🙋‍♀جستجو دختر🙋‍♀")
    markup.add("منو اصلی📜")
    bot.send_message(cid,text,reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="🎲جستجو شانسی🎲")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    dict_info_user=database.use_profile_table(cid)[0]
    list_check=[]
    for i in dict_info_user:
        list_check.append(dict_info_user[i])
    print(list_check)
    if "وارد نشده" in list_check:
        main_menu_keyboard_for_profile(cid)
    else:
        # list_profile_complet=database.use_all_profile_table()
        # list_all_profile_open=[]
        # for i in list_profile_complet:
        #     if dict_receive_direct_message[i["cid"]]=="on":
        #         list_all_profile_open.append(i["cid"])
        # if len(list_all_profile_open)==0:
        #     bot.send_message(cid,"در حال حاضر کاربری وجود ندارد لطفا بعدا امتحان کنید")
        # random_item = random.choice(list_all_profile_open)
        dict_cid_chat_anonymous.setdefault(cid,["anony","anony"])
        list_anony=[]
        for i in dict_cid_chat_anonymous:
            if i!=cid:
                if dict_cid_chat_anonymous[i][0]=="anony":
                    list_anony.append(i)
        if len(list_anony)>0:
            bot.send_message(cid,f"""
درحال جستجوی مخاطب ناشناس شما 
- {text}

لطفا صبر کنید به محض پیدا کردن بهت اطلاع میدم
""")
            random_item = int(random.choice(list_anony))
            dict_cid_chat_anonymous.pop(random_item)
            dict_cid_chat_anonymous.pop(cid)
            people_chatting_anonymous.setdefault(cid,random_item)
            people_chatting_anonymous.setdefault(random_item,cid)
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("مشاهده پروفایل مخاطب")
            markup.add("پایان چت")
            bot.send_message(random_item,"""
پیدا کردم به مخاطب وصل شدید
به مخاطب سلام کن
""",reply_markup=markup)
            bot.send_message(cid,"""
پیدا کردم به مخاطب وصل شدید
به مخاطب سلام کن
""",reply_markup=markup)
            userStep[cid]=100
            userStep[random_item]=100
        else:
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("لغو جستجو")
            bot.send_message(cid,f"""
درحال جستجوی مخاطب ناشناس شما 
- {text}

لطفا صبر کنید به محض پیدا کردن بهت اطلاع میدم
""",reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="🙋‍♀جستجو دختر🙋‍♀")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    dict_info_user=database.use_profile_table(cid)[0]
    list_check=[]
    for i in dict_info_user:
        list_check.append(dict_info_user[i])
    print(list_check)
    if "وارد نشده" in list_check:
        main_menu_keyboard_for_profile(cid)
    else:
        dict_cid_chat_anonymous.setdefault(cid,[dict_info_user["gender"],"مونث"])
        list_anony=[]
        for i in dict_cid_chat_anonymous:
            if i!=cid:
                if dict_cid_chat_anonymous[i][0]=="مونث":
                    if dict_cid_chat_anonymous[i][1]==dict_info_user["gender"]:
                        list_anony.append(i)
        if len(list_anony)>0:
            bot.send_message(cid,f"""
درحال جستجوی مخاطب ناشناس شما 
- {text}

لطفا صبر کنید به محض پیدا کردن بهت اطلاع میدم
""")
            random_item = int(random.choice(list_anony))
            dict_cid_chat_anonymous.pop(random_item)
            dict_cid_chat_anonymous.pop(cid)
            people_chatting_anonymous.setdefault(cid,random_item)
            people_chatting_anonymous.setdefault(random_item,cid)
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("مشاهده پروفایل مخاطب")
            markup.add("پایان چت")
            bot.send_message(random_item,"""
پیدا کردم به مخاطب وصل شدید
به مخاطب سلام کن
""",reply_markup=markup)
            bot.send_message(cid,"""
پیدا کردم به مخاطب وصل شدید
به مخاطب سلام کن
""",reply_markup=markup)
            userStep[cid]=100
            userStep[random_item]=100
        else:
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("لغو جستجو")
            bot.send_message(cid,f"""
درحال جستجوی مخاطب ناشناس شما 
- {text}

لطفا صبر کنید به محض پیدا کردن بهت اطلاع میدم
""",reply_markup=markup)


@bot.message_handler(func=lambda m:m.text=="🙋‍♂جستجو پسر🙋‍♂")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    dict_info_user=database.use_profile_table(cid)[0]
    list_check=[]
    for i in dict_info_user:
        list_check.append(dict_info_user[i])
    print(list_check)
    if "وارد نشده" in list_check:
        main_menu_keyboard_for_profile(cid)
    else:
        dict_cid_chat_anonymous.setdefault(cid,[dict_info_user["gender"],"مذکر"])
        list_anony=[]
        for i in dict_cid_chat_anonymous:
            if i!=cid:
                if dict_cid_chat_anonymous[i][0]=="مذکر":
                    if dict_cid_chat_anonymous[i][1]==dict_info_user["gender"]:
                        list_anony.append(i)
        if len(list_anony)>0:
            bot.send_message(cid,f"""
درحال جستجوی مخاطب ناشناس شما 
- {text}

لطفا صبر کنید به محض پیدا کردن بهت اطلاع میدم
""")
            random_item = int(random.choice(list_anony))
            dict_cid_chat_anonymous.pop(random_item)
            dict_cid_chat_anonymous.pop(cid)
            people_chatting_anonymous.setdefault(cid,random_item)
            people_chatting_anonymous.setdefault(random_item,cid)
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("مشاهده پروفایل مخاطب")
            markup.add("پایان چت")
            bot.send_message(random_item,"""
پیدا کردم به مخاطب وصل شدید
به مخاطب سلام کن
""",reply_markup=markup)
            bot.send_message(cid,"""
پیدا کردم به مخاطب وصل شدید
به مخاطب سلام کن
""",reply_markup=markup)
            userStep[cid]=100
            userStep[random_item]=100
        else:
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("لغو جستجو")
            bot.send_message(cid,f"""
درحال جستجوی مخاطب ناشناس شما 
- {text}

لطفا صبر کنید به محض پیدا کردن بهت اطلاع میدم
""",reply_markup=markup)




@bot.message_handler(func=lambda m: m.text=="مشاهده پروفایل مخاطب")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    user_id=people_chatting_anonymous[cid]
    list_dict_profile_new=database.use_profile_table(user_id)
    dict_info_profile=list_dict_profile_new[0]
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile))
    bot.send_message(user_id,"پروفایل شما توسط مخاطب مشاهده شد")
@bot.message_handler(func=lambda m: m.text=="پایان چت")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    user_id=people_chatting_anonymous[cid]
    userStep[cid]=0
    userStep[people_chatting_anonymous[cid]]=0
    people_chatting_anonymous.pop(people_chatting_anonymous[cid])
    people_chatting_anonymous.pop(cid)
    bot.send_message(cid,"""
شما چت خود با مخاطب را قطع کردید
""",reply_markup=button_nemu())
    bot.send_message(user_id,"چت شما با مخاطب توسط کاربر مقابل قطع شد",reply_markup=button_nemu())


@bot.message_handler(func=lambda m: m.text=="لغو جستجو")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    dict_cid_chat_anonymous.pop(cid)
    userStep[cid]=0
    bot.send_message(cid,"جستجو لغو شد",reply_markup=button_nemu())











@bot.message_handler(func=lambda m: m.text=="تدریس📖")

def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    userStep[cid]=0
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("دروس کنکور","دروس دانشگاهی")
    markup.add("زبان🖋","نرم افزار💻")
    markup.add("منو اصلی📜")
    bot.send_message(cid,text,reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="پارتنر علمی👨‍🎓")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    userStep[cid]=0
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("زبان","کنکور")
    markup.add("منو اصلی📜")
    bot.send_message(cid,text,reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="انجام پروژه")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    userStep[cid]=0
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("درسی و دانشگاهی","حرفه ای")
    markup.add("منو اصلی📜")
    bot.send_message(cid,text,reply_markup=markup)

@bot.message_handler(func=lambda m: m.text=="دعوت دوستان👥")
def handel_text(m):
    cid=m.chat.id
    if cid in list_admin_block:
        bot.send_message(cid,"کاربر گرامی شما مسدود شده اید")
        return
    text=m.text
    mid=m.message_id
    ID=database.use_profile_table(cid)[0]["ID"]
    bot.send_message(cid,f"""
کاربر گرامی 
در صورتی که کاربری با لینک دعوت شما وارد ربات شود هزار تومان موجودی دریافت میکنید
لینک دعوت: t.me/{bot.get_me().username}?start={ID}
""")


#-------------------------------------------------------------------userstep-------------------------------------------------------------

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def name_custom(m):
    cid = m.chat.id
    name=m.text
    database.update_profile_one_table(cid,"name",name)
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=button_inlin_edit_profile(cid))
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==2)
def name_custom(m):
    cid = m.chat.id
    age=m.text+" سال"
    database.update_profile_one_table(cid,"age",age)
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=button_inlin_edit_profile(cid))
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==3)
def name_custom(m):
    cid = m.chat.id
    height=m.text+" سانتی متر"
    database.update_profile_one_table(cid,"height",height)
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=button_inlin_edit_profile(cid))
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==4)
def name_custom(m):
    cid = m.chat.id
    weight=m.text+" کیلو"
    database.update_profile_one_table(cid,"weight",weight)
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=button_inlin_edit_profile(cid))
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==5)
def name_custom(m):
    cid = m.chat.id
    weight=m.text
    database.update_profile_one_table(cid,"province",weight)
    list_dict_profile_new=database.use_profile_table(cid)
    dict_info_profile=list_dict_profile_new[0]
    bot.send_photo(cid,dict_info_profile["photo"],text_edit_profile(dict_info_profile),reply_markup=button_inlin_edit_profile(cid))
    userStep[cid]=0
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==11)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("girlfriend",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("girlfriend",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("girlfriend",cid)
    dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_girlfriend_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_girlfriend_eboutgirl"))
    markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_girlfriend_age"))
    if database.use_post_one_table("girlfriend","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mgirlfriend"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_girlfriend
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_girlfriend"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mgirlfriend"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==12)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("girlfriend",cid,"ebout_girl",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("girlfriend",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("girlfriend",cid)
    dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_girlfriend_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_girlfriend_eboutgirl"))
    markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_girlfriend_age"))
    if database.use_post_one_table("girlfriend","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mgirlfriend"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_girlfriend
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_girlfriend"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mgirlfriend"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==13)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    userStep[cid]=0
    database.update_post_one_table("girlfriend",cid,"age_f",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("girlfriend",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("girlfriend",cid)
    dict_girl_f_cid=database.use_post_table("girlfriend",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_girlfriend_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست دختری که میخوام",callback_data="selectpost_girlfriend_eboutgirl"))
    markup.add(InlineKeyboardButton("رنج سنی دوست دخترم",callback_data="selectpost_girlfriend_age"))
    if database.use_post_one_table("girlfriend","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mgirlfriend"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_girlfriend
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_girlfriend"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mgirlfriend"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دوست دخترم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==14)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("boyfriend",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_boyfriend_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_boyfriend_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_boyfriend_age"))
    if database.use_post_one_table("boyfriend","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mboyfriend"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_boyfriend
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_boyfriend"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mboyfriend"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==15)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("boyfriend",cid,"ebout_boy",text)
    dict_info_user=database.use_profile_table(cid)[0]
    dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_boyfriend_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_boyfriend_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_boyfriend_age"))
    if database.use_post_one_table("boyfriend","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mboyfriend"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_boyfriend
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_boyfriend"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mboyfriend"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==16)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    userStep[cid]=0
    database.update_post_one_table("boyfriend",cid,"age_f",text)
    dict_info_user=database.use_profile_table(cid)[0]
    dict_girl_f_cid=database.use_post_table("boyfriend",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_boyfriend_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_boyfriend_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_boyfriend_age"))
    if database.use_post_one_table("boyfriend","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mboyfriend"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_boyfriend
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_boyfriend"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mboyfriend"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دوست پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی دوست پسرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==17)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("hhome",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_hhome_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_hhome_ebouthhome"))
    markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_hhome_ebouthome"))
    if database.use_post_one_table("hhome","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mhhome"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_hhome
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_hhome"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mhhome"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)





@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==18)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("hhome",cid,"ebout_hhome",text)
    dict_info_user=database.use_profile_table(cid)[0]
    dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_hhome_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_hhome_ebouthhome"))
    markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_hhome_ebouthome"))
    if database.use_post_one_table("hhome","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mhhome"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_hhome
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_hhome"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mhhome"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)
    
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==19)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("hhome",cid,"ebout_home",text)
    dict_info_user=database.use_profile_table(cid)[0]
    dict_girl_f_cid=database.use_post_table("hhome",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_hhome_ebout"))
    markup.add(InlineKeyboardButton("درباره دوست پسری که میخوام",callback_data="selectpost_hhome_ebouthhome"))
    markup.add(InlineKeyboardButton("رنج سنی دوست پسرم",callback_data="selectpost_hhome_ebouthome"))
    if database.use_post_one_table("hhome","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mhhome"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_hhome
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_hhome"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mhhome"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره همخونه ای که میخوام: {dict_girl_f_cid["ebout_hhome"]}
● ویژگی های خونه ای که دارم یا میخوام: {dict_girl_f_cid["ebout_home"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==20)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("sugermommy",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("sugermommy",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("sugermommy",cid)
    dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugermommy_ebout"))
    markup.add(InlineKeyboardButton("درباره پسری که میخوام",callback_data="selectpost_sugermommy_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسری که میخوام",callback_data="selectpost_sugermommy_age"))
    if database.use_post_one_table("sugermommy","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugermommy"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_sugermommy
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugermommy"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugermommy"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)


    
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==21)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("sugermommy",cid,"ebout_boy",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("sugermommy",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("sugermommy",cid)
    dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugermommy_ebout"))
    markup.add(InlineKeyboardButton("درباره پسری که میخوام",callback_data="selectpost_sugermommy_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسری که میخوام",callback_data="selectpost_sugermommy_age"))
    if database.use_post_one_table("sugermommy","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugermommy"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_sugermommy
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugermommy"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugermommy"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==22)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    userStep[cid]=0
    database.update_post_one_table("sugermommy",cid,"age_f",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("sugermommy",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("sugermommy",cid)
    dict_girl_f_cid=database.use_post_table("sugermommy",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugermommy_ebout"))
    markup.add(InlineKeyboardButton("درباره پسری که میخوام",callback_data="selectpost_sugermommy_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسری که میخوام",callback_data="selectpost_sugermommy_age"))
    if database.use_post_one_table("sugermommy","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugermommy"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_sugermommy
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugermommy"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugermommy"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسری که میخوام: {dict_girl_f_cid["ebout_boy"]}
● رنج سنی پسری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==23)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("sugerdady",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("sugerdady",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("sugerdady",cid)
    dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugerdady_ebout"))
    markup.add(InlineKeyboardButton("درباره دختری که میخوام",callback_data="selectpost_sugerdady_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی دختری که میخوام",callback_data="selectpost_sugerdady_age"))
    if database.use_post_one_table("sugerdady","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugerdady"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_sugerdady
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugerdady"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugerdady"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==24)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("sugerdady",cid,"ebout_girl",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("sugerdady",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("sugerdady",cid)
    dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugerdady_ebout"))
    markup.add(InlineKeyboardButton("درباره دختری که میخوام",callback_data="selectpost_sugerdady_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی دختری که میخوام",callback_data="selectpost_sugerdady_age"))
    if database.use_post_one_table("sugerdady","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugerdady"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_sugerdady
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugerdady"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugerdady"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==25)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    userStep[cid]=0
    database.update_post_one_table("sugerdady",cid,"age_f",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("sugerdady",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("sugerdady",cid)
    dict_girl_f_cid=database.use_post_table("sugerdady",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_sugerdady_ebout"))
    markup.add(InlineKeyboardButton("درباره دختری که میخوام",callback_data="selectpost_sugerdady_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی دختری که میخوام",callback_data="selectpost_sugerdady_age"))
    if database.use_post_one_table("sugerdady","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_msugerdady"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_sugerdady
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_sugerdady"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_msugerdady"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره دختری که میخوام: {dict_girl_f_cid["ebout_girl"]}
● رنج سنی دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==26)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("tompmarri",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("tompmarri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("tompmarri",cid)
    dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
    markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
    if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_tompmarri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_tompmarri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==27)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("tompmarri",cid,"ebout_boy_girl",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("tompmarri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("tompmarri",cid)
    dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
    markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
    if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_tompmarri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_tompmarri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==28)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("tompmarri",cid,"age_f",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("tompmarri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("tompmarri",cid)
    dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
    markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
    if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_tompmarri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_tompmarri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==29)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("tompmarri",cid,"dowry",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("tompmarri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("tompmarri",cid)
    dict_girl_f_cid=database.use_post_table("tompmarri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_tompmarri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_tompmarri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_tompmarri_age"))
    markup.add(InlineKeyboardButton("چقدر مهریه میدم/میگیرم",callback_data="selectpost_tompmarri_dowry"))
    if database.use_post_one_table("tompmarri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_tompmarri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_tompmarri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mtompmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
● چقدر مهریه میدم/میگیرم: {dict_girl_f_cid["dowry"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)
        
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==30)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("marri",cid,"ebout",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("marri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("marri",cid)
    dict_girl_f_cid=database.use_post_table("marri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_marri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_marri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_marri_age"))
    if database.use_post_one_table("marri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_marri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_marri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==31)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    userStep[cid]=0
    database.update_post_one_table("marri",cid,"ebout_boy_girl",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("marri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("marri",cid)
    dict_girl_f_cid=database.use_post_table("marri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_marri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_marri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_marri_age"))
    if database.use_post_one_table("marri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_marri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_marri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==32)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    database.update_post_one_table("marri",cid,"age_f",text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table("marri",cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table("marri",cid)
    dict_girl_f_cid=database.use_post_table("marri",cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data="selectpost_marri_ebout"))
    markup.add(InlineKeyboardButton("درباره پسر/دختری که میخوام",callback_data="selectpost_marri_eboutboy"))
    markup.add(InlineKeyboardButton("رنج سنی پسر/دختری که میخوام",callback_data="selectpost_marri_age"))
    if database.use_post_one_table("marri","post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_marri
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data="record_post_marri"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data="back_mmarri"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره من: {dict_girl_f_cid["ebout"]}
● درباره پسر/دختری که میخوام: {dict_girl_f_cid["ebout_boy_girl"]}
● رنج سنی پسر/دختری که میخوام: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)
    userStep[cid]=0










@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==33 or get_user_step(m.chat.id)==34 or get_user_step(m.chat.id)==35  
                     or get_user_step(m.chat.id)==36  or get_user_step(m.chat.id)==37  or get_user_step(m.chat.id)==38 )
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    if get_user_step(m.chat.id)==33 or get_user_step(m.chat.id)==35 or get_user_step(m.chat.id)==37:
        post_name="partnerlang"
    else:
        post_name="partnerkoo"

    if get_user_step(m.chat.id)==33 or get_user_step(m.chat.id)==34:
        key_name="ebout"
    elif get_user_step(m.chat.id)==35 or get_user_step(m.chat.id)==36:
        key_name="ebout_you"
    else:
        key_name="age_f"
    database.update_post_one_table(post_name,cid,key_name,text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table(post_name,cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table(post_name,cid)
    dict_girl_f_cid=database.use_post_table(post_name,cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{post_name}_ebout"))
    markup.add(InlineKeyboardButton("درباره پارتنری که میخوام",callback_data=f"selectpost_{post_name}_eboutyou"))
    markup.add(InlineKeyboardButton("رنج سنی پارتنرم",callback_data=f"selectpost_{post_name}_age"))
    if database.use_post_one_table(post_name,"post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{post_name}"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره پارتنری که میخوام: {dict_girl_f_cid["ebout_you"]}
● رنج سنی پارتنرم: {dict_girl_f_cid["age_f"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{post_name}
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{post_name}"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_m{post_name}"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره پارتنری که میخوام: {dict_girl_f_cid["ebout_you"]}
● رنج سنی پارتنرم: {dict_girl_f_cid["age_f"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)
    userStep[cid]=0


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==39 or get_user_step(m.chat.id)==40 or get_user_step(m.chat.id)==41  
                     or get_user_step(m.chat.id)==42  or get_user_step(m.chat.id)==43  or get_user_step(m.chat.id)==44  
                     or get_user_step(m.chat.id)==45  or get_user_step(m.chat.id)==46  or get_user_step(m.chat.id)==47  or get_user_step(m.chat.id)==48  
                     or get_user_step(m.chat.id)==49  or get_user_step(m.chat.id)==50  or get_user_step(m.chat.id)==51  or get_user_step(m.chat.id)==52  
                     or get_user_step(m.chat.id)==53  or get_user_step(m.chat.id)==54 )
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    if get_user_step(m.chat.id)==39 or get_user_step(m.chat.id)==43 or get_user_step(m.chat.id)==47 or get_user_step(m.chat.id)==51:
        post_name="teachlang"
    elif get_user_step(m.chat.id)==40 or get_user_step(m.chat.id)==44 or get_user_step(m.chat.id)==48 or get_user_step(m.chat.id)==52:
        post_name="teachkoo"
    elif get_user_step(m.chat.id)==41 or get_user_step(m.chat.id)==45 or get_user_step(m.chat.id)==49 or get_user_step(m.chat.id)==53:
        post_name="teachuniv"
    else:
        post_name="teachsys"

    if get_user_step(m.chat.id)==39 or get_user_step(m.chat.id)==40 or get_user_step(m.chat.id)==41 or get_user_step(m.chat.id)==42:
        key_name="ebout"
    elif get_user_step(m.chat.id)==43 or get_user_step(m.chat.id)==44 or get_user_step(m.chat.id)==45 or get_user_step(m.chat.id)==46:
        key_name="whatteach"
    elif get_user_step(m.chat.id)==47 or get_user_step(m.chat.id)==48 or get_user_step(m.chat.id)==49 or get_user_step(m.chat.id)==50:
        key_name="teach_exp"
    else:
        key_name="cost"
    database.update_post_one_table(post_name,cid,key_name,text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table(post_name,cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table(post_name,cid)
    dict_girl_f_cid=database.use_post_table(post_name,cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{post_name}_ebout"))
    markup.add(InlineKeyboardButton("چیزی که تدریس میکنم",callback_data=f"selectpost_{post_name}_whatteach"))
    markup.add(InlineKeyboardButton("سابقه تدریس من",callback_data=f"selectpost_{post_name}_teachexp"))
    markup.add(InlineKeyboardButton("هزینه تدریس من",callback_data=f"selectpost_{post_name}_cost"))
    if database.use_post_one_table(post_name,"post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{post_name}"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● چیزی که تدریس میکنم: {dict_girl_f_cid["whatteach"]}
● سابقه تدریس من: {dict_girl_f_cid["teach_exp"]}
● هزینه تدریس من: {dict_girl_f_cid["cost"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{post_name}
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{post_name}"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_m{post_name}"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● چیزی که تدریس میکنم: {dict_girl_f_cid["whatteach"]}
● سابقه تدریس من: {dict_girl_f_cid["teach_exp"]}
● هزینه تدریس من: {dict_girl_f_cid["cost"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)
    userStep[cid]=0


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==55 or get_user_step(m.chat.id)==56 or get_user_step(m.chat.id)==57  
                     or get_user_step(m.chat.id)==58 )
def name_custom(m):
    cid = m.chat.id
    text=m.text
    if len(text)>500:
        bot.send_message(cid,"تعداد کاراکتر بیشتر از حد مجاز است (تعداد کاراکتر مجاز 500)")
        return
    if get_user_step(m.chat.id)==55 or get_user_step(m.chat.id)==57:
        post_name="projectuinv"
    else:
        post_name="projectwork"

    print(get_user_step(m.chat.id))
    if get_user_step(m.chat.id)==55 or get_user_step(m.chat.id)==56:
        key_name="ebout"
    else:
        key_name="ecpertise"
    database.update_post_one_table(post_name,cid,key_name,text)
    dict_info_user=database.use_profile_table(cid)[0]
    list_girl_f=database.use_post_table(post_name,cid)
    if len(list_girl_f)==0:
        database.insert_post_first_table(post_name,cid)
    dict_girl_f_cid=database.use_post_table(post_name,cid)[0]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("برای ادیت کردن هر مورد روی دکمه کلیک کنید",callback_data="none"))
    markup.add(InlineKeyboardButton("درباره من",callback_data=f"selectpost_{post_name}_ebout"))
    markup.add(InlineKeyboardButton("تخصص من",callback_data=f"selectpost_{post_name}_ecpertise"))
    if database.use_post_one_table(post_name,"post",cid)[0]["post"]=="yes":
        markup.add(InlineKeyboardButton("برگشت",callback_data=f"back_m{post_name}"))
        bot.send_message(cid,f"""
ویرایش انجام شد✅
برای ویرایش هر بخش روی دکمه مربوطه کلیک کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره تخصص من: {dict_girl_f_cid["ecpertise"]}

مشاهده: /viewp_{dict_girl_f_cid['shenase']}_{post_name}
""",reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("ثبت پست",callback_data=f"record_post_{post_name}"))
        markup.add(InlineKeyboardButton("بازگشت",callback_data=f"back_m{post_name}"))
        bot.send_message(cid,f"""
{dict_info_user["name"]} عزیز
برای استفاده از این بخش و ارسال پست ابتدا باید موارد زیر را تکمیل کنید
● درباره هدف من: {dict_girl_f_cid["ebout"]}
● درباره تخصص من: {dict_girl_f_cid["ecpertise"]}
- - - - - - - - - - - - - - - - - - -
در صورت مورد تایید بودن اطلاعات بالا از دکمه 'ثبت پست' پست خود را ثبت کنید
""",reply_markup=markup)
    userStep[cid]=0




@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==100)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    bot.send_message(people_chatting_anonymous[cid],text)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==200)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    dict_info_post=database.use_post_table(dict_posend_info[cid]["post_name"],dict_posend_info[cid]["uid"])[0]
    ID=database.use_profile_table(cid)[0]["ID"]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ارسال پیام",callback_data=f"ansposend_{cid}_{dict_posend_info[cid]["post_name"]}"))
    bot.send_message(dict_posend_info[cid]["uid"],f"""
پیام جدید
پروفایل کاربر: /user_{ID}
پست: /viewp_{dict_info_post['shenase']}_{dict_posend_info[cid]["post_name"]}
➖➖➖➖➖➖➖➖➖
{text}
""",reply_markup=markup)
    bot.send_message(cid,"پیام شما ارسال شد")
    if cid in people_chatting_anonymous:
        userStep[cid]=100
    else:
        userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==201)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    dict_info_post=database.use_post_table(dict_posend_info[cid]["post_name"],dict_posend_info[cid]["uid"])[0]
    ID=database.use_profile_table(cid)[0]["ID"]
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ارسال پیام",callback_data=f"posend_{cid}_{dict_posend_info[cid]["post_name"]}"))
    bot.send_message(dict_posend_info[cid]["uid"],f"""
پیام جدید
پروفایل کاربر: /user_{ID}
پست: /viewp_{dict_info_post['shenase']}_{dict_posend_info[cid]["post_name"]}
➖➖➖➖➖➖➖➖➖
{text}
""",reply_markup=markup)
    bot.send_message(cid,"پیام شما ارسال شد")
    if cid in people_chatting_anonymous:
        userStep[cid]=100
    else:
        userStep[cid]=0



@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1000)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    mid=m.message_id
    list_user=database.use_all_profile()
    count=0
    count_black=0
    for i in list_user:
        try:
            bot.copy_message(i["cid"],cid,mid)
            count+=1
        except:
            pass
            # database.delete_users(i)
            # count_black+=1
            # print("eror")
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
    text=f"به {count} نفر ارسال شد"
    # if count_black!=0:
    #     text=f"\n و به {count_black} نفر ارسال نشد احتمالا ربات را بلاک کرده اند و از دیتابیس ما حذف میشوند \n"
    bot.send_message(cid,text,reply_markup=markup)
    userStep[cid]=0
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1001)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    mid=m.message_id
    list_user=database.use_all_profile()
    count=0
    for i in list_user:
        try:
            bot.forward_message(i["cid"],cid,mid)
            count+=1
        except:
            pass
            # databases.delete_users(i)
            # count_black+=1
            # print("eror")
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
    text=f"به {count} نفر فوروارد شد"
    # if count_black!=0:
    #     text=f"\n و به {count_black} نفر ارسال نشد احتمالا ربات را بلاک کرده اند و از دیتابیس ما حذف میشوند \n"
    bot.send_message(cid,text,reply_markup=markup)
    userStep[cid]=0

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1003)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    mid=m.message_id
    if text.isdigit():
        database.add_validity(dict_validity["ID"],int(text))
        dict_info=database.use_profile_id_table(dict_validity["ID"])[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
        bot.send_message(cid,f"""
موجودی با موفقیت افزایش پیدا کرد
موجودی حال حاضر کاربر /user_{dict_validity["ID"]} 
{dict_info["validity"]} تومان است
""",reply_markup=markup)
        userStep[cid]=0
    else:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لغو و بازگشت به پنل",callback_data="admin_back_panel"))
        bot.send_message(cid,"لطفا برای افزایش اعتبار فقط عدد انگلیسی ارسال کنید:",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1004)
def name_custom(m):
    cid = m.chat.id
    text=m.text
    mid=m.message_id
    if text.isdigit():
        database.sub_validity(dict_validity["ID"],int(text))
        dict_info=database.use_profile_id_table(dict_validity["ID"])[0]
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_panel"))
        bot.send_message(cid,f"""
موجودی با موفقیت کاهش پیدا کرد
موجودی حال حاضر کاربر /user_{dict_validity["ID"]} 
{dict_info["validity"]} تومان است
""",reply_markup=markup)
        userStep[cid]=0
    else:
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("لغو و بازگشت به پنل",callback_data="admin_back_panel"))
        bot.send_message(cid,"لطفا برای کاهش اعتبار فقط عدد انگلیسی ارسال کنید:",reply_markup=markup)


@bot.message_handler(func=lambda m: True)
def product(m):
    cid = m.chat.id
    # bot.send_message(cid, "مقدار وارد شده نامعتبر است ")
bot.infinity_polling()
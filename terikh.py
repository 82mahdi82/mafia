from datetime import datetime, timedelta
import jdatetime
import pytz

# تنظیم منطقه زمانی برای ایران
tehran_timezone = pytz.timezone('Asia/Tehran')
# تاریخ امروز
current_date = jdatetime.datetime.now(tehran_timezone)

def dict_time_now():
# نام روزهای هفته به زبان فارسی
    persian_weekdays = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
    dict_time={}
    # چاپ تاریخ‌های هفته از امروز تا 7 روز بعد به شمسی و به زبان فارسی
    for i in range(8):
        future_date = current_date + timedelta(days=i)
        persian_day_name = persian_weekdays[future_date.weekday()]
        # persian_date = jdatetime.date.strftime(future_date,"%m")
        dict_time.setdefault(persian_day_name,jdatetime.date.strftime(future_date,"%Y/%m/%d"))
        # print(persian_day_name, ":", persian_date)
    return dict_time
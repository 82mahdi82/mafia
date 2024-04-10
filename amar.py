import matplotlib.pyplot as plt
from collections import Counter

# لیست داده‌ها
# data = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]

def get_Amounts(data):
# شمارش تعداد تکرار هر عدد
    counter = Counter(data)

    # انتخاب مقادیر و تعداد تکرارها برای استفاده در نمودار
    labels = list(counter.keys())
    sizes = list(counter.values())

    fig, (ax1, ax2) = plt.subplots(1, 2)


    ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax1.set_title("Pie Chart")
    # رسم نمودار
    ax2.bar(labels, sizes)
    ax2.set_xlabel("Amounts")
    ax2.set_ylabel('number of users')
    ax2.set_title("Bar Chart")

    # ذخیره کردن نمودار به صورت فایل PNG
    plt.savefig('bar_chart.png')

    return 'bar_chart.png'
    # plt.show()

# import matplotlib.pyplot as plt
# from collections import Counter

# # لیست داده‌ها
# data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]

# # شمارش تعداد تکرار هر عدد
# counter = Counter(data)

# # انتخاب مقادیر و تعداد تکرارها برای استفاده در نمودارها
# labels = list(counter.keys())
# sizes = list(counter.values())

# # ایجاد شکل با دو نمودار کنار هم
# fig, (ax1, ax2) = plt.subplots(1, 2)

# # نمودار دایره ای
# ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
# ax1.set_title('نمودار دایره ای تعداد تکرار مقادیر در لیست')

# # نمودار میله‌ای
# ax2.bar(labels, sizes)
# ax2.set_xlabel('مقادیر')
# ax2.set_ylabel('تعداد تکرار')
# ax2.set_title('نمودار میله ای تعداد تکرار مقادیر در لیست')

# # ذخیره کردن نمودارها به صورت فایل PNG
# plt.savefig('combined_charts.png')

# # نمایش نمودارها
# plt.show()


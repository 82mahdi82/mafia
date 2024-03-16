import instaloader

def download_post(post_id):
    # ساخت یک نمونه از کلاس Instaloader
    loader = instaloader.Instaloader()

    try:
        # دریافت اطلاعات پست با استفاده از آی‌دی
        post = instaloader.Post.from_shortcode(loader.context, post_id)
        
        # دانلود تصویر پست
        loader.download_post(post, target='.')
        
        print("پست با موفقیت دانلود شد.")
    except Exception as e:
        print("خطا در دریافت پست:", e)

# آی‌دی پست مورد نظر را وارد کنید
post_id = "CfW7aLUosdz"  # آی‌دی پست اینستاگرام

# دانلود پست
download_post(post_id)

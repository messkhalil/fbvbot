def generate_fdown_link(fb_url):
    """إنشاء رابط تحميل مباشر من fdown.net"""
    return f"https://fdown.net/?url={fb_url}"

def download_facebook_video(url):
    """الدالة الرئيسية التي تُرجع رابط fdown.net"""
    if 'facebook.com' not in url and 'fb.watch' not in url:
        raise Exception("❌ هذا ليس رابط فيسبوك صحيح.")
    return generate_fdown_link(url)

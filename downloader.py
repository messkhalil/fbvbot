import os
import yt_dlp
from config import DOWNLOAD_FOLDER, MAX_FILE_SIZE

def setup_download_dir():
    """إنشاء مجلد التحميل إذا لم يكن موجودًا"""
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

def clean_filename(filename):
    """تنظيف اسم الملف من الأحرف غير المسموح بها"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_via_ytdlp(url):
    """تحميل الفيديو عبر yt-dlp باستخدام الكوكيز"""
    try:
        setup_download_dir()
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'max_filesize': MAX_FILE_SIZE,
            'cookiefile': 'cookies.txt',  # ✅ ملفات الكوكيز
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            file_size = os.path.getsize(filename)
            if file_size > MAX_FILE_SIZE:
                os.remove(filename)
                raise Exception(f"حجم الفيديو كبير جدًا ({file_size//(1024*1024)}MB). الحد الأقصى هو {MAX_FILE_SIZE//(1024*1024)}MB")

            return filename

    except Exception as e:
        raise Exception(f"فشل التحميل عبر yt-dlp: {str(e)}")

def download_facebook_video(url):
    """الدالة الرئيسية لتحميل فيديوهات فيسبوك"""
    try:
        if 'facebook.com' not in url and 'fb.watch' not in url:
            raise Exception("الرجاء إدخال رابط فيسبوك صحيح")

        return download_via_ytdlp(url)

    except Exception as e:
        raise Exception(f"فشل التحميل: {str(e)}")

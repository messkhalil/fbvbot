import os
import requests
from bs4 import BeautifulSoup
from config import DOWNLOAD_FOLDER, MAX_FILE_SIZE

def setup_download_dir():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

def clean_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_from_fdown(url):
    """تحميل فيديو فيسبوك باستخدام موقع fdown.net"""
    try:
        setup_download_dir()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.post("https://fdown.net/download.php", data={"URLz": url}, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # نحاول إيجاد أفضل جودة
        best_link = soup.find("a", string="HD Video")
        if not best_link:
            best_link = soup.find("a", string="Normal Video")

        if not best_link:
            raise Exception("فشل استخراج رابط الفيديو من الموقع.")

        video_url = best_link["href"]
        video_data = requests.get(video_url, headers=headers, stream=True)
        video_data.raise_for_status()

        filename = clean_filename("facebook_video.mp4")
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            for chunk in video_data.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)

        file_size = os.path.getsize(filepath)
        if file_size > MAX_FILE_SIZE:
            os.remove(filepath)
            raise Exception(f"الفيديو أكبر من الحد المسموح ({file_size//(1024*1024)}MB)")

        return filepath

    except Exception as e:
        raise Exception(f"فشل التحميل من fdown.net: {str(e)}")

def download_facebook_video(url):
    """الدالة الرئيسية للتحميل"""
    try:
        if 'facebook.com' not in url and 'fb.watch' not in url:
            raise Exception("الرجاء إدخال رابط فيسبوك صحيح")

        return download_from_fdown(url)

    except Exception as e:
        raise Exception(f"فشل التحميل: {str(e)}")

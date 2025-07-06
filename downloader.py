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

def download_facebook_video(fb_url):
    """يحاول استخراج رابط مباشر من fdown.net وتحميل الفيديو"""
    try:
        setup_download_dir()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.post(
            "https://fdown.net/download.php",
            data={"URLz": fb_url},
            headers=headers
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # نحاول جلب الفيديو عالي الجودة أولاً
        hd_link = soup.find("a", string="HD Video")
        sd_link = soup.find("a", string="Normal Video")

        video_url = None
        if hd_link:
            video_url = hd_link["href"]
        elif sd_link:
            video_url = sd_link["href"]

        if not video_url:
            raise Exception("❌ لم يتم العثور على رابط الفيديو في fdown.net")

        # تحميل الفيديو
        video_response = requests.get(video_url, headers=headers, stream=True)
        video_response.raise_for_status()

        filename = clean_filename("facebook_video.mp4")
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            for chunk in video_response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)

        file_size = os.path.getsize(filepath)
        if file_size > MAX_FILE_SIZE:
            os.remove(filepath)
            raise Exception(f"الفيديو أكبر من الحد ({file_size // (1024*1024)}MB)")

        return filepath

    except Exception as e:
        raise Exception(f"فشل تحميل الفيديو: {str(e)}")

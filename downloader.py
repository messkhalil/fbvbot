import os
import requests
import yt_dlp
from config import DOWNLOAD_FOLDER

def download_facebook_video(url):
    try:
        # الطريقة الأولى: yt-dlp مع إعدادات خاصة
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'extractor_args': {
                    'facebook': {
                        'skip_dash_manifest': True,
                        'referer': 'https://www.facebook.com'
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0',
                    'Referer': 'https://www.facebook.com'
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
                
        except Exception as yt_err:
            print(f"Failed with yt-dlp: {yt_err}")
            # الطريقة الثانية: استخدام API خارجي
            return download_via_api(url)
            
    except Exception as e:
        raise Exception(f"فشل التحميل: {str(e)}")

def download_via_api(url):
    """استخدام API خارجي كبديل"""
    try:
        # مثال باستخدام API مجاني (قد يحتاج لتحديث)
        api_url = "https://getvideobot.com/api/v1/facebook"
        response = requests.post(api_url, json={"url": url})
        response.raise_for_status()
        
        video_url = response.json().get("download_url")
        if not video_url:
            raise Exception("لا يوجد رابط تحميل في الاستجابة")
            
        # تنزيل الفيديو
        video_data = requests.get(video_url, stream=True)
        filename = os.path.join(DOWNLOAD_FOLDER, "fb_video.mp4")
        
        with open(filename, 'wb') as f:
            for chunk in video_data.iter_content(chunk_size=1024):
                f.write(chunk)
                
        return filename
        
    except Exception as e:
        raise Exception(f"فشل التحميل عبر API: {str(e)}")

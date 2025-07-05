import os
import yt_dlp
from config import DOWNLOAD_FOLDER, MAX_FILE_SIZE

def download_facebook_video(url):
    try:
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'max_filesize': MAX_FILE_SIZE,
            'extractor_args': {
                'facebook': {
                    'skip_dash_manifest': True,
                    'referer': 'https://www.facebook.com'
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename

    except Exception as e:
        raise Exception(f"فشل التحميل: {str(e)}")

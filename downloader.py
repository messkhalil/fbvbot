from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def download_with_selenium(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options
        )
        
        driver.get(url)
        time.sleep(10)  # انتظر حتى يتم تحميل الفيديو
        
        video_element = driver.find_element_by_tag_name('video')
        video_url = video_element.get_attribute('src')
        
        if not video_url:
            raise Exception("لم يتم العثور على رابط الفيديو")
            
        # استمر في عملية التحميل...
        
    except Exception as e:
        raise Exception(f"خطأ في Selenium: {str(e)}")

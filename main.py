from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from downloader import download_facebook_video
from config import BOT_TOKEN, DOWNLOAD_FOLDER
import os
import shutil

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دالة الترحيب"""
    welcome_msg = """
مرحبًا بك في بوت تحميل فيديوهات الفيسبوك!

📌 فقط أرسل رابط الفيديو من الفيسبوك وسأقوم بتحميله لك.

⚙️ الميزات:
- يدعم معظم روابط الفيسبوك
- يحافظ على الجودة الأصلية
- يدعم الفيديوهات الطويلة (حتى 50MB)
    """
    await update.message.reply_text(welcome_msg)

async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة طلب تحميل الفيديو"""
    user = update.message.from_user
    print(f"طلب تحميل من {user.first_name} (@{user.username}): {update.message.text}")
    
    if not update.message.text:
        await update.message.reply_text("⚠️ يرجى إرسال رابط الفيديو فقط")
        return
    
    try:
        # إعلام المستخدم بأن البوت يعمل على التحميل
        status_msg = await update.message.reply_text("⏳ جاري تحميل الفيديو...")
        
        # تحميل الفيديو
        video_path = download_facebook_video(update.message.text)
        
        # إرسال الفيديو
        await update.message.reply_video(
            video=open(video_path, 'rb'),
            caption="✅ تم تحميل الفيديو بنجاح",
            supports_streaming=True,
            width=1280,
            height=720
        )
        
        # حذف الرسالة المؤقتة
        await context.bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=status_msg.message_id
        )
        
        # حذف الفيديو المؤقت
        os.remove(video_path)
        
    except Exception as e:
        error_msg = f"❌ حدث خطأ أثناء التحميل: {str(e)}"
        await update.message.reply_text(error_msg)
        print(error_msg)

def cleanup():
    """تنظيف الملفات المؤقتة عند إيقاف البوت"""
    if os.path.exists(DOWNLOAD_FOLDER):
        shutil.rmtree(DOWNLOAD_FOLDER)

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # تسجيل الدوال
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_request))
    
    # تنظيف الملفات عند الإغلاق
    import atexit
    atexit.register(cleanup)
    
    # بدء البوت
    print("🤖 البوت يعمل...")
    application.run_polling()

if __name__ == '__main__':
    main()
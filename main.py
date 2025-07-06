from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from downloader import download_facebook_video
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة الترحيب"""
    welcome_msg = """
مرحبًا بك في بوت تحميل فيديوهات الفيسبوك!
تم تطويره من طرف @Kh_xd

📌 فقط أرسل رابط الفيديو من فيسبوك، وسأرسل لك رابط التحميل اليدوي من fdown.net.
⚠️ ملاحظة: لا يمكن تحميل الفيديو مباشرة بسبب قيود الاستضافة.
    """
    await update.message.reply_text(welcome_msg)

async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة رابط الفيديو"""
    user = update.message.from_user
    print(f"طلب من {user.first_name} (@{user.username}): {update.message.text}")

    if not update.message.text:
        await update.message.reply_text("⚠️ أرسل رابط الفيديو فقط.")
        return

    try:
        status_msg = await update.message.reply_text("⏳ جاري معالجة الرابط...")

        fdown_link = download_facebook_video(update.message.text)

        await update.message.reply_text(
            f"✅ تم إنشاء رابط التحميل:\n\n{fdown_link}\n\n"
            f"📥 افتحه في متصفحك لتحميل الفيديو."
        )

        await context.bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=status_msg.message_id
        )

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
        print(f"[❌] {str(e)}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_request))
    print("🤖 البوت يعمل الآن...")
    application.run_polling()

if __name__ == "__main__":
    main()

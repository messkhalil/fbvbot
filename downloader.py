async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة طلب تحميل الفيديو"""
    user = update.message.from_user
    print(f"طلب تحميل من {user.first_name} (@{user.username}): {update.message.text}")
    
    if not update.message.text:
        await update.message.reply_text("⚠️ يرجى إرسال رابط الفيديو فقط")
        return

    try:
        status_msg = await update.message.reply_text("⏳ جاري معالجة الرابط...")

        video_path = download_facebook_video(update.message.text)

        # إرسال الرابط فقط بدل تحميل الفيديو
        await update.message.reply_text(
            f"⚠️ لا يمكن تحميل فيديو فيسبوك مباشرة داخل البوت.\n📥 لكن يمكنك تحميله يدويًا من الرابط التالي:\n\n{video_path}"
        )

        await context.bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=status_msg.message_id
        )

    except Exception as e:
        error_msg = f"❌ حدث خطأ أثناء التحميل: {str(e)}"
        await update.message.reply_text(error_msg)
        print(error_msg)

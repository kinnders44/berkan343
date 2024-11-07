# bot.py
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from datetime import datetime

# Config importları
from config import (
    BOT_TOKEN, USER_STATS, REFERRAL_BONUS,
    TOPIC, LENGTH, STYLE, WATERMARK, MUSIC, TEMPLATE
)

# Utils importları
from utils import save_data, load_data

# Admin importları
from admin import (
    admin, add_credits_admin, remove_credits_admin,
    sales_report, list_users, top_users,
    notify_user, broadcast
)

# Video importları
from video import (
    create, preview_video, handle_edit_callback, create_final_video,
    get_length_text, get_music_details, get_watermark_info,
    check_credits, check_preview_limit, get_preview_duration
)

# Payment importları
from payment import balance, buy, payment, confirm_payment

# Referral importları
from referral import handle_referral, referral, load_referral_data

# Profil importları
from user_profile import show_profile, show_video_archive, update_settings

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update, context):
    """Bot başlangıç fonksiyonu"""
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name
    
    # Yeni kullanıcı kontrolü
    if user_id not in USER_STATS:
        USER_STATS[user_id] = {
            'join_date': str(datetime.now()),
            'videos_created': 0,
            'total_spent': 0
        }
        save_data()
    
    # Referans kontrolü
    if len(context.args) > 0:
        handle_referral(update, context)
    
    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    
    update.message.reply_text(f"""
    👋 Merhaba {user_name}! Video Oluşturma Botuna Hoş Geldin!
    
    📝 Temel Komutlar:
    /create - Yeni video oluştur (1 kredi)
    /balance - Kredi bakiyeni gör
    /buy - Kredi satın al
    
    👤 Profil İşlemleri:
    /profile - Profilini gör
    /videos - Video arşivin
    /settings - Ayarları düzenle
    
    🎁 Referans Programı:
    /referral - Referans bilgilerin
    • Arkadaşlarını davet et, {REFERRAL_BONUS['inviter']} kredi kazan!
    • Davet ettiğin kişi {REFERRAL_BONUS['invited']} kredi kazansın!
    
    🔗 Senin Referans Linkin:
    {referral_link}
    """)

def main():
    """Bot ana fonksiyonu"""
    logger.info("Bot başlatılıyor...")
    
    # Verileri yükle
    load_data()
    load_referral_data()
    
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Video oluşturma conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create)],
        states={
            TOPIC: [MessageHandler(Filters.text & ~Filters.command, create)],
            LENGTH: [MessageHandler(Filters.text & ~Filters.command, create)],
            STYLE: [MessageHandler(Filters.text & ~Filters.command, create)],
            WATERMARK: [MessageHandler(Filters.text & ~Filters.command, create)],
            MUSIC: [MessageHandler(Filters.text & ~Filters.command, create)],
            TEMPLATE: [MessageHandler(Filters.text & ~Filters.command, create)]
        },
        fallbacks=[CommandHandler('cancel', lambda u,c: ConversationHandler.END)]
    )

    # Temel komutlar
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("payment", payment))
    dp.add_handler(MessageHandler(Filters.regex('^/confirm$'), confirm_payment))

    # Profil komutları
    dp.add_handler(CommandHandler("profile", show_profile))
    dp.add_handler(CommandHandler("videos", show_video_archive))
    dp.add_handler(CommandHandler("settings", update_settings))

    # Referral komutları
    dp.add_handler(CommandHandler("referral", referral))

    # Admin komutları
    dp.add_handler(CommandHandler("admin", admin))
    dp.add_handler(CommandHandler("addcredits", add_credits_admin))
    dp.add_handler(CommandHandler("removecredits", remove_credits_admin))
    dp.add_handler(CommandHandler("sales", sales_report))
    dp.add_handler(CommandHandler("users", list_users))
    dp.add_handler(CommandHandler("topusers", top_users))
    dp.add_handler(CommandHandler("notify", notify_user))
    dp.add_handler(CommandHandler("broadcast", broadcast))

    # Preview ve edit handlers
    dp.add_handler(CommandHandler("preview", preview_video))
    dp.add_handler(CallbackQueryHandler(handle_edit_callback))

    # Video oluşturma handler'ı
    dp.add_handler(conv_handler)

    # Botu başlat
    updater.start_polling()
    logger.info("Bot başarıyla başlatıldı!")
    updater.idle()

if __name__ == '__main__':
    main()
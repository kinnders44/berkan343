# video.py
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import time
import json
from datetime import datetime, timedelta
from config import (
    TOPIC, LENGTH, STYLE, WATERMARK, MUSIC, TEMPLATE,
    VIDEO_STYLES, MUSIC_TYPES, VIDEO_FORMATS,
    BASE_DIR, TEMP_DIR, LOGO_DIR, AUDIO_DIR, VIDEO_DIR,
    USER_CREDITS, USER_STATS, PREVIEW_LIMITS
)
from utils import save_data
from user_profile import get_profile, update_profile_stats

logger = logging.getLogger(__name__)
TEST_MODE = True

# Klasör kontrolü
for dir_path in [TEMP_DIR, LOGO_DIR, AUDIO_DIR, VIDEO_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Önizleme sayaçları
PREVIEW_COUNTS = {}

def check_credits(user_id: str) -> int:
    return USER_CREDITS.get(str(user_id), 0)

def check_preview_limit(user_id: str) -> bool:
    user_id = str(user_id)
    current_time = datetime.now()
    profile = get_profile(user_id)
    package_type = profile.get('package_type', 'basic')
    
    # Premium sınırsız önizleme
    if package_type == 'premium':
        return True
    
    # Günlük limit kontrolü
    if user_id not in PREVIEW_COUNTS:
        PREVIEW_COUNTS[user_id] = {
            'count': 0,
            'reset_time': current_time + timedelta(days=1)
        }
    
    # Gün değiştiyse sıfırla
    if current_time >= PREVIEW_COUNTS[user_id]['reset_time']:
        PREVIEW_COUNTS[user_id] = {
            'count': 0,
            'reset_time': current_time + timedelta(days=1)
        }
    
    # Limit kontrolü
    daily_limit = PREVIEW_LIMITS[package_type]['daily_limit']
    if PREVIEW_COUNTS[user_id]['count'] >= daily_limit:
        return False
    
    PREVIEW_COUNTS[user_id]['count'] += 1
    return True

def get_preview_duration(user_id: str) -> int:
    profile = get_profile(user_id)
    package_type = profile.get('package_type', 'basic')
    return PREVIEW_LIMITS[package_type]['duration']

def create(update: Update, context: CallbackContext) -> int:
    user_id = str(update.message.from_user.id)
    profile = get_profile(user_id)
    package_type = profile.get('package_type', 'basic')
    
    if check_credits(user_id) > 0:
        preview_limit = PREVIEW_LIMITS[package_type]['daily_limit']
        preview_duration = PREVIEW_LIMITS[package_type]['duration']
        
        limit_text = "Sınırsız" if preview_limit == -1 else str(preview_limit)
        
        update.message.reply_text(f"""
        🎥 Yeni Video Oluşturma
        
        📝 Video için konu başlığını yazar mısın?
        Örnek: 'Yapay Zeka Nedir?'
        
        ℹ️ Önizleme Bilgileri:
        • Paketiniz: {package_type.upper()}
        • Günlük Limit: {limit_text} önizleme
        • Önizleme Süresi: {preview_duration} saniye
        
        🛠️ Komutlar:
        • /preview - Önizleme al
        • /cancel - İptal et
        """)
        return TOPIC
    else:
        update.message.reply_text("""
        ❌ Yetersiz kredi!
        
        💰 Kredi satın almak için /balance yazabilirsiniz.
        🎁 Veya arkadaşlarını davet ederek /referral bedava kredi kazanabilirsin!
        """)
        return ConversationHandler.END

def preview_video(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    
    if not context.user_data.get('topic'):
        update.message.reply_text("❌ Önce video oluşturmaya başlayın: /create")
        return
    
    if not check_preview_limit(user_id):
        profile = get_profile(user_id)
        package_type = profile.get('package_type', 'basic')
        limit = PREVIEW_LIMITS[package_type]['daily_limit']
        
        update.message.reply_text(f"""
        ❌ Günlük önizleme limitiniz doldu!
        
        📊 Paket Bilgileri:
        • Paketiniz: {package_type.upper()}
        • Günlük Limit: {limit} önizleme
        
        ⭐️ Daha fazla önizleme için:
        • Pro Paket: Günde 10 önizleme
        • Premium Paket: Sınırsız önizleme
        
        /upgrade - Paket yükselt
        """)
        return
    try:
        preview_duration = get_preview_duration(user_id)
        
        # Önizleme bilgileri
        preview_text = f"""
        🎥 Video Önizleme ({preview_duration} saniye)
        
        📝 İçerik:
        • Başlık: {context.user_data['topic']}
        • Uzunluk: {get_length_text(context.user_data.get('length', '1'))}
        • Stil: {VIDEO_STYLES[context.user_data.get('style', '1')]}
        
        🎨 Görsel:
        • Format: {VIDEO_FORMATS[context.user_data.get('template', '1')]}
        • Watermark: {get_watermark_info(context.user_data)}
        
        🎵 Ses:
        • Müzik: {get_music_details(context.user_data.get('music'))}
        
        ⚙️ Düzenleme:
        • /edit_text - Metni düzenle
        • /edit_style - Stili değiştir
        • /edit_music - Müziği değiştir
        """
        
        keyboard = [
            [
                InlineKeyboardButton("✏️ Düzenle", callback_data="edit_video"),
                InlineKeyboardButton("✅ Onayla", callback_data="confirm_video")
            ]
        ]
        
        if TEST_MODE:
            update.message.reply_text(
                preview_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            # Gerçek önizleme videosu oluştur
            pass
            
    except Exception as e:
        logger.error(f"Preview error: {e}")
        update.message.reply_text("""
        ❌ Önizleme oluşturulamadı!
        Lütfen tüm seçimleri yaptığınızdan emin olun.
        """)

def get_length_text(length_choice: str) -> str:
    lengths = {
        '1': '30 saniye',
        '2': '1 dakika',
        '3': '2 dakika'
    }
    return lengths.get(length_choice, 'Bilinmiyor')

def get_music_details(music_data: dict) -> str:
    if not music_data:
        return "Müzik yok"
    elif isinstance(music_data, dict):
        if music_data['type'] == 'youtube':
            return "YouTube müzik"
        elif music_data['type'] == 'spotify':
            return "Spotify müzik"
        elif music_data['type'] == 'file':
            return "Özel müzik"
    return "Bilinmeyen müzik"

def get_watermark_info(user_data: dict) -> str:
    if 'watermark_type' not in user_data:
        return "Yok"
    
    wtype = user_data['watermark_type']
    if wtype == '1':
        return "Logo"
    elif wtype == '2':
        return f"Metin: {user_data.get('watermark_text', '')}"
    elif wtype == '3':
        return f"Logo + Metin: {user_data.get('watermark_text', '')}"
    else:
        return "Yok"

def handle_edit_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    
    if query.data == "edit_video":
        keyboard = [
            [InlineKeyboardButton("📝 Metin", callback_data="edit_text")],
            [InlineKeyboardButton("🎨 Stil", callback_data="edit_style")],
            [InlineKeyboardButton("🎵 Müzik", callback_data="edit_music")],
            [InlineKeyboardButton("📐 Format", callback_data="edit_format")]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif query.data == "confirm_video":
        query.edit_message_text("""
        ✅ Video onaylandı!
        
        🎬 Video oluşturuluyor...
        ⏳ Tahmini süre: 2-3 dakika
        
        Hazır olunca size haber vereceğim!
        """)
        # Video oluşturma işlemini başlat
        create_final_video(context.user_data, query.from_user.id, context)

def create_final_video(video_data: dict, user_id: str, context: CallbackContext) -> None:
    try:
        if TEST_MODE:
            time.sleep(5)  # Video oluşturma simülasyonu
            context.bot.send_message(
                chat_id=user_id,
                text="""
                ✨ Videonuz hazır!
                
                📥 Video indirme linki:
                example.com/video123
                
                📊 Video İstatistikleri:
                • Süre: 2:30
                • Boyut: 15MB
                • Kalite: 1080p
                
                🎁 Yeni video oluşturmak için:
                /create komutunu kullanabilirsiniz
                """
            )
    except Exception as e:
        logger.error(f"Video creation error: {e}")
        context.bot.send_message(
            chat_id=user_id,
            text="❌ Video oluşturulurken bir hata oluştu!"
        )
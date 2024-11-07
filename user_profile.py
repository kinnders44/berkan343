# user_profile.py
from config import LANGUAGES
from utils import save_data
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

# Global user profiles dictionary
USER_PROFILES = {}

class UserProfile:
    def __init__(self, user_id, username=None):
        self.user_id = str(user_id)
        self.username = username
        self.language = 'tr'
        self.created_at = str(datetime.now())
        self.videos = []
        self.settings = {
            'notifications': True,
            'auto_preview': True,
            'default_format': '9:16',
            'watermark': None,
            'preferred_voice': None
        }
        self.stats = {
            'total_videos': 0,
            'total_credits_used': 0,
            'total_spent': 0,
            'last_video_date': None
        }

def initialize_profiles():
    """Load existing profiles or create new storage"""
    try:
        with open('user_profiles.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for user_id, profile_data in data.items():
                profile = UserProfile(user_id)
                profile.__dict__.update(profile_data)
                USER_PROFILES[user_id] = profile
        logger.info("User profiles loaded successfully")
    except FileNotFoundError:
        logger.info("No existing profiles found, starting fresh")
    except Exception as e:
        logger.error(f"Error loading profiles: {e}")

def save_profiles():
    """Save all user profiles"""
    try:
        profiles_data = {
            user_id: profile.__dict__ 
            for user_id, profile in USER_PROFILES.items()
        }
        with open('user_profiles.json', 'w', encoding='utf-8') as f:
            json.dump(profiles_data, f, ensure_ascii=False, indent=4)
        logger.info("User profiles saved successfully")
    except Exception as e:
        logger.error(f"Error saving profiles: {e}")

def get_profile(user_id):
    """Get or create user profile"""
    user_id = str(user_id)
    if user_id not in USER_PROFILES:
        USER_PROFILES[user_id] = UserProfile(user_id)
        save_profiles()
    return USER_PROFILES[user_id]

def update_profile_stats(user_id, video_data):
    """Update user statistics after video creation"""
    profile = get_profile(user_id)
    profile.stats['total_videos'] += 1
    profile.stats['total_credits_used'] += 1
    profile.stats['last_video_date'] = str(datetime.now())
    profile.videos.append({
        'id': len(profile.videos) + 1,
        'title': video_data.get('topic', 'Untitled'),
        'date': str(datetime.now()),
        'format': video_data.get('template'),
        'length': video_data.get('length'),
        'style': video_data.get('style')
    })
    save_profiles()

def show_profile(update, context):
    """Display user profile"""
    user_id = str(update.message.from_user.id)
    profile = get_profile(user_id)
    
    recent_videos = get_recent_videos(profile)
    
    update.message.reply_text(f"""
    👤 Profil Bilgileri
    
    🆔 ID: {user_id}
    🌍 Dil: {LANGUAGES[profile.language]['flag']} {LANGUAGES[profile.language]['name']}
    📅 Katılım: {profile.created_at[:10]}
    
    📊 İstatistikler:
    • Toplam Video: {profile.stats['total_videos']}
    • Kullanılan Kredi: {profile.stats['total_credits_used']}
    • Toplam Harcama: {profile.stats['total_spent']}₺
    • Son Video: {profile.stats['last_video_date'][:10] if profile.stats['last_video_date'] else 'Yok'}
    
    🎥 Son Videolar:
    {recent_videos}
    
    ⚙️ Ayarlar:
    • Bildirimler: {'✅' if profile.settings['notifications'] else '❌'}
    • Otomatik Önizleme: {'✅' if profile.settings['auto_preview'] else '❌'}
    • Tercih Edilen Format: {profile.settings['default_format']}
    
    📝 Komutlar:
    /settings - Ayarları düzenle
    /videos - Video arşivi
    /stats - Detaylı istatistikler
    """)

def get_recent_videos(profile, limit=3):
    """Format recent videos"""
    if not profile.videos:
        return "Henüz video oluşturulmamış"
    
    recent = profile.videos[-limit:]
    result = ""
    for video in recent:
        date = video['date'].split()[0]
        result += f"• {video['title']} ({date})\n"
    return result

def show_video_archive(update, context):
    """Display user's video archive"""
    user_id = str(update.message.from_user.id)
    profile = get_profile(user_id)
    
    if not profile.videos:
        update.message.reply_text("�empty Henüz video oluşturmamışsınız!")
        return
    
    videos_per_page = 5
    page = context.args[0] if context.args else 1
    try:
        page = int(page)
    except:
        page = 1
    
    start_idx = (page - 1) * videos_per_page
    end_idx = start_idx + videos_per_page
    page_videos = profile.videos[start_idx:end_idx]
    
    message = "🎥 Video Arşivi\n\n"
    for video in page_videos:
        message += f"""
        📹 {video['title']}
        📅 Tarih: {video['date'].split()[0]}
        📐 Format: {video['format']}
        ⏱️ Uzunluk: {video['length']}
        🎨 Stil: {video['style']}
        ---------------
        """
    
    total_pages = (len(profile.videos) + videos_per_page - 1) // videos_per_page
    message += f"\nSayfa {page}/{total_pages}"
    
    update.message.reply_text(message)

def update_settings(update, context):
    """Update user settings"""
    user_id = str(update.message.from_user.id)
    profile = get_profile(user_id)
    
    setting = context.args[0] if context.args else None
    value = context.args[1] if len(context.args) > 1 else None
    
    if not setting or not value:
        update.message.reply_text("""
        ⚙️ Ayarları Düzenle
        
        Kullanım: /settings [ayar] [değer]
        
        Mevcut Ayarlar:
        • notifications [on/off]
        • auto_preview [on/off]
        • default_format [9:16/1:1/16:9]
        """)
        return
    
    try:
        if setting == 'notifications':
            profile.settings['notifications'] = (value.lower() == 'on')
        elif setting == 'auto_preview':
            profile.settings['auto_preview'] = (value.lower() == 'on')
        elif setting == 'default_format':
            if value in ['9:16', '1:1', '16:9']:
                profile.settings['default_format'] = value
        
        save_profiles()
        update.message.reply_text("✅ Ayarlar güncellendi!")
        
    except Exception as e:
        logger.error(f"Settings update error: {e}")
        update.message.reply_text("❌ Ayarlar güncellenirken hata oluştu!")

# Initialize profiles when module is imported
initialize_profiles()
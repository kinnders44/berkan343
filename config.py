# config.py
import os

# Bot Token
BOT_TOKEN = "7809770400:AAGjzrbgoc9eU0qRuM61NB63ETKSPCzUbF8"

# Admin Listesi
ADMIN_LIST = [7991156675, '7991156675']

# Conversation States (Durum Kodları)
TOPIC, LENGTH, STYLE = range(3)  # 0, 1, 2
WATERMARK, MUSIC, TEMPLATE = range(3, 6)  # 3, 4, 5
VOICE_SELECT, EMOTION_SELECT, SPEED_SELECT, EMPHASIS_SELECT = range(10, 14)  # 10, 11, 12, 13
PAYMENT_METHOD, PAYMENT_CONFIRM = range(20, 22)  # 20, 21

# Kredi Paketleri
CREDIT_PACKAGES = {
    "basic": {
        "credits": 20,
        "price": "299₺",
        "bonus": 2,
        "features": ["720p", "Temel Şablonlar"]
    },
    "pro": {
        "credits": 50,
        "price": "599₺",
        "bonus": 5,
        "features": ["1080p", "Tüm Şablonlar", "Özel Watermark"]
    },
    "premium": {
        "credits": 100,
        "price": "999₺",
        "bonus": 10,
        "features": ["4K", "Tüm Özellikler", "Öncelikli Destek", "Özel Müzik"]
    }
}

# Referans Sistemi
REFERRAL_BONUS = {
    "inviter": 3,  # Davet eden kişiye verilecek kredi
    "invited": 2   # Davet edilen kişiye verilecek kredi
}

# Video Ayarları
VIDEO_STYLES = {
    '1': 'Modern ve Dinamik',
    '2': 'Profesyonel ve Kurumsal',
    '3': 'Eğlenceli ve Renkli',
    '4': 'Minimal ve Şık',
    '5': 'Vintage ve Retro'
}

MUSIC_TYPES = {
    '1': 'Enerjik Pop',
    '2': 'Kurumsal',
    '3': 'Duygusal',
    '4': 'Motivasyon',
    '5': 'Ambient',
    '6': 'Müzik Yok'
}

VIDEO_FORMATS = {
    '1': 'Instagram Story (9:16)',
    '2': 'YouTube Short (9:16)',
    '3': 'TikTok (9:16)',
    '4': 'Instagram Post (1:1)',
    '5': 'YouTube Video (16:9)',
    '6': 'LinkedIn (16:9)',
    '7': 'Twitter (16:9)'
}

# Ses Ayarları
VOICE_LIBRARY = {
    'tr_male': {
        '1': {'name': 'Ahmet', 'style': 'professional', 'age': '30-40'},
        '2': {'name': 'Mehmet', 'style': 'young', 'age': '20-30'},
        '3': {'name': 'Ali', 'style': 'warm', 'age': '40-50'},
        '4': {'name': 'Can', 'style': 'energetic', 'age': '25-35'}
    },
    'tr_female': {
        '5': {'name': 'Ayşe', 'style': 'professional', 'age': '30-40'},
        '6': {'name': 'Zeynep', 'style': 'young', 'age': '20-30'},
        '7': {'name': 'Elif', 'style': 'warm', 'age': '35-45'},
        '8': {'name': 'Seda', 'style': 'energetic', 'age': '25-35'}
    },
    'en_male': {
        '9': {'name': 'John', 'style': 'professional', 'age': '35-45'},
        '10': {'name': 'Mike', 'style': 'casual', 'age': '25-35'}
    },
    'en_female': {
        '11': {'name': 'Sarah', 'style': 'professional', 'age': '30-40'},
        '12': {'name': 'Emma', 'style': 'young', 'age': '20-30'}
    }
}

VOICE_EMOTIONS = {
    '1': 'Nötr',
    '2': 'Mutlu',
    '3': 'Enerjik',
    '4': 'Profesyonel',
    '5': 'Samimi'
}

VOICE_SPEEDS = {
    '1': 'Çok Yavaş',
    '2': 'Yavaş',
    '3': 'Normal',
    '4': 'Hızlı',
    '5': 'Çok Hızlı'
}

# Önizleme Limitleri
PREVIEW_LIMITS = {
    'basic': {'daily_limit': 3, 'duration': 3},
    'pro': {'daily_limit': 10, 'duration': 5},
    'premium': {'daily_limit': -1, 'duration': 7}  # -1 = sınırsız
}

# Dil Ayarları
LANGUAGES = {
    'tr': {
        'name': 'Türkçe',
        'flag': '🇹🇷',
        'strings': {
            'welcome': 'Hoş geldiniz!',
            'select_language': 'Lütfen dilinizi seçin:',
            'language_changed': 'Diliniz değiştirildi: {}'
        }
    },
    'en': {
        'name': 'English',
        'flag': '🇬🇧',
        'strings': {
            'welcome': 'Welcome!',
            'select_language': 'Please select your language:',
            'language_changed': 'Language changed to: {}'
        }
    }
}

DEFAULT_LANGUAGE = 'tr'

# Dosya Yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
LOGO_DIR = os.path.join(BASE_DIR, "user_logos")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "videos")

# Veri Yapıları (Runtime'da doldurulacak)
USER_CREDITS = {}  # Kullanıcı kredileri
USER_STATS = {}    # Kullanıcı istatistikleri
REFERRAL_DATA = {} # Referans verileri
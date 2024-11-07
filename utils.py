# utils.py
import json
import logging
import os
from datetime import datetime
from typing import Optional, Tuple, List

from config import (
    USER_STATS, USER_CREDITS, REFERRAL_DATA,
    TEMP_DIR, LOGO_DIR, AUDIO_DIR, VIDEO_DIR
)

logger = logging.getLogger(__name__)

def ensure_directories() -> None:
    """Gerekli klasörlerin varlığını kontrol et ve oluştur"""
    directories = [TEMP_DIR, LOGO_DIR, AUDIO_DIR, VIDEO_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                logger.info(f"Directory created: {directory}")
            except Exception as e:
                logger.error(f"Error creating directory {directory}: {e}")

def save_data() -> bool:
    """Tüm verileri kaydet"""
    try:
        data = {
            'credits': USER_CREDITS,
            'stats': USER_STATS,
            'referrals': REFERRAL_DATA,
            'last_update': str(datetime.now())
        }
        
        with open('bot_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        logger.info("Data saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False

def load_data() -> bool:
    """Tüm verileri yükle"""
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            global USER_CREDITS, USER_STATS, REFERRAL_DATA
            USER_CREDITS = data.get('credits', {})
            USER_STATS = data.get('stats', {})
            REFERRAL_DATA = data.get('referrals', {})
            
        logger.info("Data loaded successfully")
        return True
    except FileNotFoundError:
        logger.info("No existing data found, starting fresh")
        return True
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return False

def clean_temp_files() -> bool:
    """Geçici dosyaları temizle"""
    try:
        for directory in [TEMP_DIR, LOGO_DIR, AUDIO_DIR]:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    if (datetime.now() - datetime.fromtimestamp(os.path.getctime(file_path))).days >= 1:
                        os.remove(file_path)
        logger.info("Temp files cleaned successfully")
        return True
    except Exception as e:
        logger.error(f"Error cleaning temp files: {e}")
        return False

def format_time(seconds: int) -> str:
    """Saniyeyi okunabilir formata çevir"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{int(hours)}s {int(minutes)}d {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}d {int(seconds)}s"
    else:
        return f"{int(seconds)}s"

def format_size(size_bytes: int) -> str:
    """Byte'ı okunabilir formata çevir"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}GB"

def validate_file(file_path: str, max_size_mb: int = 10, allowed_extensions: Optional[List[str]] = None) -> Tuple[bool, str]:
    """Dosya kontrolü yap"""
    try:
        if not os.path.exists(file_path):
            return False, "Dosya bulunamadı"
            
        file_size = os.path.getsize(file_path)
        if file_size > max_size_mb * 1024 * 1024:
            return False, f"Dosya boyutu çok büyük (Max: {max_size_mb}MB)"
            
        if allowed_extensions:
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in allowed_extensions:
                return False, f"Desteklenmeyen dosya formatı (İzin verilenler: {', '.join(allowed_extensions)})"
                
        return True, "OK"
    except Exception as e:
        logger.error(f"File validation error: {e}")
        return False, "Dosya kontrolünde hata oluştu"

def backup_data() -> Tuple[bool, str]:
    """Verilerin yedeğini al"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_data_{timestamp}.json'
        
        data = {
            'credits': USER_CREDITS,
            'stats': USER_STATS,
            'referrals': REFERRAL_DATA,
            'backup_date': str(datetime.now())
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        logger.info(f"Backup created: {backup_file}")
        return True, backup_file
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return False, str(e)

def restore_backup(backup_file: str) -> Tuple[bool, str]:
    """Yedeği geri yükle"""
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            global USER_CREDITS, USER_STATS, REFERRAL_DATA
            USER_CREDITS = data.get('credits', {})
            USER_STATS = data.get('stats', {})
            REFERRAL_DATA = data.get('referrals', {})
            
        save_data()
        logger.info(f"Backup restored: {backup_file}")
        return True, "Yedek başarıyla geri yüklendi"
    except Exception as e:
        logger.error(f"Restore error: {e}")
        return False, str(e)
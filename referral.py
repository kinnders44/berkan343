# referral.py
from config import USER_STATS, USER_CREDITS, REFERRAL_DATA, REFERRAL_BONUS
from utils import save_data
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def save_referral_data():
    """Referans verilerini kaydet"""
    try:
        with open('referral_data.json', 'w') as f:
            json.dump(REFERRAL_DATA, f)
        logger.info("Referral data saved successfully")
    except Exception as e:
        logger.error(f"Error saving referral data: {e}")

def load_referral_data():
    """Referans verilerini yükle"""
    try:
        with open('referral_data.json', 'r') as f:
            global REFERRAL_DATA
            REFERRAL_DATA = json.load(f)
        logger.info("Referral data loaded successfully")
    except FileNotFoundError:
        logger.info("No referral data found, starting fresh")
    except Exception as e:
        logger.error(f"Error loading referral data: {e}")

def add_credits(user_id, amount):
    """Kullanıcıya kredi ekle"""
    USER_CREDITS[str(user_id)] = USER_CREDITS.get(str(user_id), 0) + amount
    save_data()

def handle_referral(update, context):
    """Referans işlemlerini yönet"""
    try:
        user_id = str(update.message.from_user.id)
        user_name = update.message.from_user.first_name
        referrer_id = context.args[0]

        # Kendini refere edemez
        if referrer_id == user_id:
            return

        # Daha önce refere edilmemiş olmalı
        if user_id in REFERRAL_DATA.get(referrer_id, []):
            return

        # Referans eden kişi sistemde kayıtlı olmalı
        if referrer_id in USER_CREDITS:
            # Referans listesini güncelle
            if referrer_id not in REFERRAL_DATA:
                REFERRAL_DATA[referrer_id] = []
            REFERRAL_DATA[referrer_id].append(user_id)

            # Kredileri ekle
            add_credits(referrer_id, REFERRAL_BONUS['inviter'])
            add_credits(user_id, REFERRAL_BONUS['invited'])

            # İstatistikleri güncelle
            if referrer_id in USER_STATS:
                USER_STATS[referrer_id]['referrals'] = len(REFERRAL_DATA[referrer_id])

            # Bildirimleri gönder
            context.bot.send_message(
                chat_id=referrer_id,
                text=f"""
                🎉 Yeni Referans!
                
                👤 {user_name} davetinizle katıldı
                💰 {REFERRAL_BONUS['inviter']} kredi kazandınız!
                
                /balance ile bakiyenizi kontrol edin
                """
            )

            update.message.reply_text(f"""
            🎁 Hoş geldiniz!
            
            Referans bonusu olarak {REFERRAL_BONUS['invited']} kredi kazandınız!
            /balance ile bakiyenizi kontrol edebilirsiniz
            """)

            # Verileri kaydet
            save_referral_data()
            save_data()

    except Exception as e:
        logger.error(f"Referral handling error: {e}")

def referral(update, context):
    """Referans bilgilerini göster"""
    user_id = str(update.message.from_user.id)
    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    
    # Referans istatistikleri
    referrals = REFERRAL_DATA.get(user_id, [])
    total_referrals = len(referrals)
    total_earned = total_referrals * REFERRAL_BONUS['inviter']
    
    update.message.reply_text(f"""
    🎁 Referans Programı
    
    📊 İstatistikleriniz:
    • Toplam Davet: {total_referrals} kişi
    • Kazanılan Kredi: {total_earned}
    
    💰 Referans Bonusları:
    • Sen kazanırsın: {REFERRAL_BONUS['inviter']} kredi
    • Arkadaşın kazanır: {REFERRAL_BONUS['invited']} kredi
    
    🔗 Senin Referans Linkin:
    {referral_link}
    
    📝 Nasıl Çalışır?
    1. Referans linkini arkadaşlarınla paylaş
    2. Arkadaşın bota katıldığında otomatik bonus kazanırsın
    3. Arkadaşın da bonus kredilerle başlar
    
    ⭐️ Ne kadar çok davet o kadar çok kredi!
    """)

def get_referral_stats(user_id):
    """Kullanıcının referans istatistiklerini getir"""
    referrals = REFERRAL_DATA.get(str(user_id), [])
    return {
        'total_referrals': len(referrals),
        'total_earned': len(referrals) * REFERRAL_BONUS['inviter'],
        'referral_list': referrals
    }

def get_top_referrers(limit=5):
    """En çok referans yapanları getir"""
    referrer_stats = []
    for user_id, refs in REFERRAL_DATA.items():
        referrer_stats.append({
            'user_id': user_id,
            'referral_count': len(refs),
            'total_earned': len(refs) * REFERRAL_BONUS['inviter']
        })
    
    return sorted(
        referrer_stats,
        key=lambda x: x['referral_count'],
        reverse=True
    )[:limit]
# payment.py
from telegram.ext import ConversationHandler
from config import (
    CREDIT_PACKAGES, USER_STATS, REFERRAL_DATA, 
    ADMIN_LIST, PAYMENT_CONFIRM, REFERRAL_BONUS
)
from utils import save_data
from admin import check_credits, add_credits
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Ödeme durumları için sabitler
PAYMENT_METHODS = ['havale', 'kart', 'kripto']
PAYMENT_STATUS = {
    'PENDING': 'pending',
    'COMPLETED': 'completed',
    'FAILED': 'failed'
}

def save_pending_payment(user_id, package, method, amount):
    """Bekleyen ödemeyi kaydet"""
    try:
        payment_data = {
            'user_id': str(user_id),
            'package': package,
            'method': method,
            'amount': amount,
            'status': PAYMENT_STATUS['PENDING'],
            'date': str(datetime.now())
        }
        logger.info(f"Pending payment saved: {payment_data}")
        return True
    except Exception as e:
        logger.error(f"Payment save error: {e}")
        return False

def buy(update, context):
    """Paket satın alma komutu"""
    try:
        package = context.args[0].lower()
        if package in CREDIT_PACKAGES:
            update.message.reply_text(f"""
            🛒 {package.upper()} Paketi seçtiniz
            
            💳 Ödeme yapmak için:
            • Havale/EFT
            • Kredi Kartı
            • Kripto
            
            Ödeme yöntemi seçmek için:
            /payment {package} havale
            /payment {package} kart
            /payment {package} kripto
            """)
        else:
            update.message.reply_text("❌ Geçersiz paket! Lütfen /balance yazarak paketleri görüntüleyin.")
    except Exception as e:
        logger.error(f"Buy command error: {e}")
        update.message.reply_text("❌ Lütfen bir paket seçin. Örnek: /buy basic")

def payment(update, context):
    """Ödeme işlemi başlat"""
    try:
        package, method = context.args
        if package in CREDIT_PACKAGES and method in PAYMENT_METHODS:
            amount = CREDIT_PACKAGES[package]['price']
            credits = CREDIT_PACKAGES[package]['credits']
            
            if method == 'havale':
                update.message.reply_text(f"""
                🏦 Havale/EFT Bilgileri:
                
                Banka: X Bankası
                IBAN: TR12 3456 7890
                Ad Soyad: Video Bot
                Tutar: {amount}
                
                Açıklama: {update.message.from_user.id}
                
                ℹ️ Ödeme yaptıktan sonra /confirm yazın
                💝 {credits} kredi hesabınıza eklenecek
                """)
            
            elif method == 'kart':
                update.message.reply_text(f"""
                💳 Kredi Kartı Ödemesi
                
                🔗 Ödeme Linki: payment.videobot.com/{update.message.from_user.id}
                Tutar: {amount}
                
                ℹ️ Link üzerinden ödeme yapabilirsiniz
                💝 Ödeme onayı otomatik gelecek
                """)
            
            elif method == 'kripto':
                update.message.reply_text(f"""
                🪙 Kripto Ödeme Bilgileri:
                
                USDT (TRC20): TRX...
                BTC: BTC...
                ETH: ETH...
                
                Tutar: {amount}
                
                ℹ️ Ödeme yaptıktan sonra /confirm yazın
                💝 {credits} kredi hesabınıza eklenecek
                """)
            
            context.user_data['pending_package'] = package
            save_pending_payment(update.message.from_user.id, package, method, amount)
            return PAYMENT_CONFIRM
            
    except Exception as e:
        logger.error(f"Payment error: {e}")
        update.message.reply_text("❌ Hatalı komut! Örnek: /payment basic havale")

def confirm_payment(update, context):
    """Ödeme onayı"""
    user_id = str(update.message.from_user.id)
    
    if 'pending_package' in context.user_data:
        package = context.user_data['pending_package']
        credits = CREDIT_PACKAGES[package]['credits']
        bonus = CREDIT_PACKAGES[package]['bonus']
        total_credits = credits + bonus
        
        try:
            # Kredileri ekle
            add_credits(user_id, total_credits)
            
            # İstatistikleri güncelle
            if user_id in USER_STATS:
                USER_STATS[user_id]['total_spent'] += int(CREDIT_PACKAGES[package]['price'].replace('₺', ''))
                save_data()
            
            # Admin'lere bildirim
            for admin in ADMIN_LIST:
                try:
                    context.bot.send_message(
                        chat_id=admin,
                        text=f"""
                        💰 Yeni Ödeme!
                        
                        👤 Kullanıcı: {user_id}
                        📦 Paket: {package.upper()}
                        💎 Kredi: {credits} + {bonus} bonus
                        💵 Tutar: {CREDIT_PACKAGES[package]['price']}
                        """
                    )
                except Exception as e:
                    logger.error(f"Admin notification error: {e}")
                    continue
            
            update.message.reply_text(f"""
            ✅ Ödemeniz onaylandı!
            
            📦 Paket: {package.upper()}
            💝 {credits} kredi + {bonus} bonus = {total_credits} kredi
            
            🎥 Hemen video oluşturmaya başlayabilirsiniz:
            /create - Yeni video oluştur
            /balance - Bakiye kontrol
            """)
            
            del context.user_data['pending_package']
            return ConversationHandler.END
            
        except Exception as e:
            logger.error(f"Payment confirmation error: {e}")
            update.message.reply_text("❌ Ödeme onaylanırken bir hata oluştu!")
            return ConversationHandler.END
    else:
        update.message.reply_text("❌ Bekleyen ödeme bulunamadı!")

def balance(update, context):
    """Bakiye ve paket bilgilerini göster"""
    user_id = str(update.message.from_user.id)
    credits = check_credits(user_id)
    referral_count = len(REFERRAL_DATA.get(user_id, []))
    total_earned = referral_count * REFERRAL_BONUS['inviter']
    
    update.message.reply_text(f"""
    💰 Hesap Durumu
    
    🎥 Kredi Bakiyeniz: {credits} video
    👥 Referans Sayınız: {referral_count}
    🎁 Referans Kazancı: {total_earned} kredi
    
    📦 PAKETLER:
    
    🔵 BASIC PAKET
    • {CREDIT_PACKAGES['basic']['credits']} Video Kredisi
    • 720p Kalite
    • Temel Şablonlar
    • Fiyat: {CREDIT_PACKAGES['basic']['price']}
    • Bonus: {CREDIT_PACKAGES['basic']['bonus']} kredi
    
    🟣 PRO PAKET
    • {CREDIT_PACKAGES['pro']['credits']} Video Kredisi
    • 1080p Kalite
    • Tüm Şablonlar
    • Özel Watermark
    • Fiyat: {CREDIT_PACKAGES['pro']['price']}
    • Bonus: {CREDIT_PACKAGES['pro']['bonus']} kredi
    
    ⭐️ PREMIUM PAKET
    • {CREDIT_PACKAGES['premium']['credits']} Video Kredisi
    • 4K Kalite
    • Tüm Özellikler
    • Öncelikli Destek
    • Özel Müzik Yükleme
    • Fiyat: {CREDIT_PACKAGES['premium']['price']}
    • Bonus: {CREDIT_PACKAGES['premium']['bonus']} kredi
    
    Satın almak için: /buy basic, /buy pro veya /buy premium
    """)
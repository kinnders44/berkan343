# admin.py
from config import ADMIN_LIST, USER_STATS, USER_CREDITS, REFERRAL_DATA
from utils import save_data
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def check_credits(user_id):
    """Kullanıcı kredilerini kontrol et"""
    return USER_CREDITS.get(str(user_id), 0)

def add_credits(user_id, amount):
    """Kullanıcıya kredi ekle"""
    USER_CREDITS[str(user_id)] = USER_CREDITS.get(str(user_id), 0) + amount
    save_data()

def is_admin(user_id):
    """Admin kontrolü"""
    return str(user_id) in map(str, ADMIN_LIST)

def admin(update, context):
    """Admin paneli"""
    if not is_admin(update.message.from_user.id):
        update.message.reply_text("❌ Bu komut sadece adminler içindir!")
        return

    total_users = len(USER_STATS)
    total_videos = sum(stats['videos_created'] for stats in USER_STATS.values())
    total_revenue = sum(stats['total_spent'] for stats in USER_STATS.values())
    total_referrals = sum(len(refs) for refs in REFERRAL_DATA.values())

    update.message.reply_text(f"""
    👑 Admin Panel
    
    📊 Genel İstatistikler:
    • Toplam Kullanıcı: {total_users}
    • Oluşturulan Video: {total_videos}
    • Toplam Gelir: {total_revenue}₺
    • Toplam Referans: {total_referrals}
    
    📝 Komutlar:
    
    💰 Kredi İşlemleri:
    /addcredits [user_id] [miktar] - Kredi ekle
    /removecredits [user_id] [miktar] - Kredi sil
    
    📊 Raporlar:
    /sales - Detaylı satış raporu
    /users - Kullanıcı listesi
    /topusers - En aktif kullanıcılar
    
    📨 İletişim:
    /broadcast - Toplu mesaj gönder
    /notify - Özel bildirim gönder
    """)

def add_credits_admin(update, context):
    """Admin kredi ekleme"""
    if not is_admin(update.message.from_user.id):
        update.message.reply_text("❌ Bu komut sadece adminler içindir!")
        return
    
    try:
        user_id = context.args[0]
        amount = int(context.args[1])
        add_credits(user_id, amount)
        update.message.reply_text(f"""
        ✅ Kredi eklendi!
        👤 Kullanıcı: {user_id}
        💰 Eklenen: {amount}
        💎 Yeni bakiye: {check_credits(user_id)}
        """)
    except Exception as e:
        logger.error(f"Kredi ekleme hatası: {e}")
        update.message.reply_text("❌ Hata! Örnek: /addcredits user_id miktar")

def remove_credits_admin(update, context):
    """Admin kredi silme"""
    if not is_admin(update.message.from_user.id):
        update.message.reply_text("❌ Bu komut sadece adminler içindir!")
        return
    
    try:
        user_id = context.args[0]
        amount = int(context.args[1])
        current_credits = check_credits(user_id)
        if current_credits >= amount:
            USER_CREDITS[user_id] = current_credits - amount
            save_data()
            update.message.reply_text(f"""
            ✅ Kredi silindi!
            👤 Kullanıcı: {user_id}
            💰 Silinen: {amount}
            💎 Yeni bakiye: {check_credits(user_id)}
            """)
        else:
            update.message.reply_text("❌ Yetersiz kredi!")
    except Exception as e:
        logger.error(f"Kredi silme hatası: {e}")
        update.message.reply_text("❌ Hata! Örnek: /removecredits user_id miktar")

def list_users(update, context):
    """Kullanıcı listesi"""
    if not is_admin(update.message.from_user.id):
        return
    
    user_list = ""
    for user_id in USER_STATS:
        stats = USER_STATS[user_id]
        credits = check_credits(user_id)
        user_list += f"""
👤 ID: {user_id}
💰 Krediler: {credits}
🎥 Videolar: {stats['videos_created']}
💵 Harcama: {stats['total_spent']}₺
📅 Katılım: {stats['join_date']}
---------------"""
    
    update.message.reply_text(f"📊 Kullanıcı Listesi:\n{user_list}")

def notify_user(update, context):
    """Özel kullanıcıya mesaj gönder"""
    if not is_admin(update.message.from_user.id):
        return
    
    try:
        user_id = context.args[0]
        message = ' '.join(context.args[1:])
        
        context.bot.send_message(
            chat_id=user_id,
            text=f"📢 Admin Mesajı:\n\n{message}"
        )
        
        update.message.reply_text("✅ Mesaj gönderildi!")
    except Exception as e:
        logger.error(f"Mesaj gönderme hatası: {e}")
        update.message.reply_text("❌ Hata! Örnek: /notify user_id mesaj")

def broadcast(update, context):
    """Toplu mesaj gönder"""
    if not is_admin(update.message.from_user.id):
        return
    
    try:
        message = ' '.join(context.args)
        success = 0
        failed = 0
        
        for user_id in USER_STATS:
            try:
                context.bot.send_message(chat_id=user_id, text=message)
                success += 1
            except:
                failed += 1
        
        update.message.reply_text(f"""
        📨 Broadcast Tamamlandı
        
        ✅ Başarılı: {success}
        ❌ Başarısız: {failed}
        """)
    except Exception as e:
        logger.error(f"Broadcast hatası: {e}")
        update.message.reply_text("❌ Hata! Örnek: /broadcast mesaj")

def sales_report(update, context):
    """Satış raporu"""
    if not is_admin(update.message.from_user.id):
        return

    try:
        total_users = len(USER_STATS)
        total_videos = sum(stats['videos_created'] for stats in USER_STATS.values())
        total_spent = sum(stats['total_spent'] for stats in USER_STATS.values())
        
        update.message.reply_text(f"""
        📊 Satış Raporu
        
        👥 Kullanıcı İstatistikleri:
        • Toplam Kullanıcı: {total_users}
        • Toplam Video: {total_videos}
        • Toplam Gelir: {total_spent}₺
        
        💰 Ortalamalar:
        • Video/Kullanıcı: {total_videos/total_users if total_users > 0 else 0:.1f}
        • Gelir/Kullanıcı: {total_spent/total_users if total_users > 0 else 0:.1f}₺
        """)
    except Exception as e:
        logger.error(f"Satış raporu hatası: {e}")
        update.message.reply_text("❌ Rapor oluşturulurken hata oluştu!")

def top_users(update, context):
    """En aktif kullanıcılar"""
    if not is_admin(update.message.from_user.id):
        return
        
    try:
        # En çok video oluşturanlar
        video_ranking = sorted(
            USER_STATS.items(),
            key=lambda x: x[1]['videos_created'],
            reverse=True
        )[:5]
        
        # En çok harcama yapanlar
        spending_ranking = sorted(
            USER_STATS.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )[:5]
        
        message = "🏆 EN AKTİF KULLANICILAR\n\n"
        message += "🎥 Video Sıralaması:\n"
        for i, (user_id, stats) in enumerate(video_ranking, 1):
            message += f"{i}. ID: {user_id} - {stats['videos_created']} video\n"
        
        message += "\n💰 Harcama Sıralaması:\n"
        for i, (user_id, stats) in enumerate(spending_ranking, 1):
            message += f"{i}. ID: {user_id} - {stats['total_spent']}₺\n"
        
        update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Top users hatası: {e}")
        update.message.reply_text("❌ Sıralama oluşturulurken hata oluştu!")
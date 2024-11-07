# template_gallery.py
from config import TEMPLATE_GALLERY
import logging

logger = logging.getLogger(__name__)

def show_gallery(update, context):
    """Şablon galerisini göster"""
    update.message.reply_text("""
    🎨 Şablon Galerisi
    
    📱 Stories (9:16):
    • Modern Story - Dinamik ve çarpıcı
    • Business Story - Profesyonel ve şık
    
    📷 Posts (1:1):
    • Minimal Post - Sade ve etkileyici
    • Dynamic Post - Hareketli ve modern
    
    🎥 Videos (16:9):
    • Classic Video - Geleneksel format
    • Cinematic - Sinematik görünüm
    
    Önizleme için: /preview [şablon_id]
    Favori eklemek için: /favorite [şablon_id]
    """)

def preview_template(update, context):
    """Şablon önizleme"""
    try:
        template_id = context.args[0]
        # Şablon videosunu gönder
        update.message.reply_video(
            video=open(f'templates/{template_id}.mp4', 'rb'),
            caption="🎥 Şablon Önizleme"
        )
    except:
        update.message.reply_text("❌ Şablon bulunamadı!")
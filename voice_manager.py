# voice_manager.py
from config import VOICE_LIBRARY
import logging

logger = logging.getLogger(__name__)

class VoiceManager:
    def __init__(self):
        self.voices = VOICE_LIBRARY
        self.emotions = {
            '1': 'Nötr',
            '2': 'Mutlu',
            '3': 'Enerjik',
            '4': 'Profesyonel',
            '5': 'Samimi',
            '6': 'Heyecanlı'
        }
        self.speeds = {
            '1': 'Çok Yavaş',
            '2': 'Yavaş',
            '3': 'Normal',
            '4': 'Hızlı',
            '5': 'Çok Hızlı'
        }
        self.emphasis = {
            '1': 'Hafif',
            '2': 'Orta',
            '3': 'Güçlü'
        }

    def get_voice_menu(self):
        """Ses seçim menüsünü oluştur"""
        menu = """
🎤 Profesyonel Seslendirme Seçenekleri:

👨 Erkek Sesleri (Türkçe):
1. Ahmet - Profesyonel (30-40 yaş)
2. Mehmet - Genç (20-30 yaş)
3. Ali - Sıcak (40-50 yaş)
4. Can - Enerjik (25-35 yaş)
5. Murat - Derin (35-45 yaş)
6. Burak - Samimi (30-40 yaş)
7. Kemal - Otoriter (45-55 yaş)
8. Deniz - Günlük (25-35 yaş)

👩 Kadın Sesleri (Türkçe):
9. Ayşe - Profesyonel (30-40 yaş)
10. Zeynep - Genç (20-30 yaş)
11. Elif - Sıcak (35-45 yaş)
12. Seda - Enerjik (25-35 yaş)
13. Merve - Yumuşak (30-40 yaş)
14. Ceyda - Samimi (25-35 yaş)
15. Aslı - Profesyonel (35-45 yaş)
16. Yağmur - Günlük (20-30 yaş)

🗣️ İngilizce Sesler için /en yazın

⚙️ Ses Ayarları:
/emotion - Duygu seç
/speed - Hız ayarla
/emphasis - Vurgu ayarla

🎭 Özel Seçenekler:
/clone - Kendi sesinizi klonlayın
/preview [numara] - Ses önizleme

💡 Her ses için örnek dinleyebilirsiniz!
"""
        return menu

    def get_emotion_menu(self):
        """Duygu seçim menüsü"""
        menu = "🎭 Duygu Seçin:\n\n"
        for key, emotion in self.emotions.items():
            menu += f"{key}. {emotion}\n"
        return menu

    def get_speed_menu(self):
        """Hız seçim menüsü"""
        menu = "⚡ Konuşma Hızı:\n\n"
        for key, speed in self.speeds.items():
            menu += f"{key}. {speed}\n"
        return menu

    def get_emphasis_menu(self):
        """Vurgu seçim menüsü"""
        menu = "💪 Vurgu Seviyesi:\n\n"
        for key, emphasis in self.emphasis.items():
            menu += f"{key}. {emphasis}\n"
        return menu

    def preview_voice(self, voice_id, text=None, emotion=None, speed=None, emphasis=None):
        """Ses önizleme oluştur"""
        try:
            # Burada ElevenLabs API çağrısı yapılacak
            preview_text = text or "Merhaba! Ben sizin seçtiğiniz ses. Videoyu bu ses ile seslendireceğim."
            # API çağrısı ve ses dosyası oluşturma
            return "preview_audio.mp3"  # Örnek dönüş
        except Exception as e:
            logger.error(f"Ses önizleme hatası: {e}")
            return None

    def clone_voice(self, voice_file):
        """Ses klonlama"""
        try:
            # Burada ElevenLabs Voice Cloning API çağrısı yapılacak
            return True, "cloned_voice_id"
        except Exception as e:
            logger.error(f"Ses klonlama hatası: {e}")
            return False, str(e)
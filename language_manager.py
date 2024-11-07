# language_manager.py
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from config import LANGUAGES, DEFAULT_LANGUAGE
from user_profile import get_profile, save_profiles
import logging

logger = logging.getLogger(__name__)

SELECTING_LANGUAGE = range(1)

def get_string(user_id, key):
    """Get string in user's language"""
    try:
        profile = get_profile(user_id)
        lang = profile.language
        return LANGUAGES[lang]['strings'].get(key, LANGUAGES[DEFAULT_LANGUAGE]['strings'][key])
    except:
        return LANGUAGES[DEFAULT_LANGUAGE]['strings'][key]

def show_language_menu(update, context):
    """Show language selection menu"""
    keyboard = []
    for lang_code, lang_data in LANGUAGES.items():
        keyboard.append([f"{lang_data['flag']} {lang_data['name']}"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "🌍 Dil seçimi / Language selection:\n\n"
        "🇹🇷 Lütfen dilinizi seçin\n"
        "🇬🇧 Please select your language",
        reply_markup=reply_markup
    )
    return SELECTING_LANGUAGE

def handle_language_selection(update, context):
    """Handle language selection"""
    text = update.message.text
    user_id = str(update.message.from_user.id)
    
    selected_lang = None
    for lang_code, lang_data in LANGUAGES.items():
        if lang_data['flag'] in text:
            selected_lang = lang_code
            break
    
    if selected_lang:
        profile = get_profile(user_id)
        profile.language = selected_lang
        save_profiles()
        
        update.message.reply_text(
            f"✅ Diliniz değiştirildi / Language changed: "
            f"{LANGUAGES[selected_lang]['flag']} {LANGUAGES[selected_lang]['name']}",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "❌ Geçersiz seçim / Invalid selection\n"
            "Lütfen listeden seçin / Please select from the list"
        )
        return SELECTING_LANGUAGE
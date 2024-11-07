# api_config.py

# API Keys (Production'da environment variables kullanılacak)
API_KEYS = {
    'openai': 'YOUR_OPENAI_API_KEY',
    'stable_diffusion': 'YOUR_SD_API_KEY',
    'elevenlabs': 'YOUR_ELEVENLABS_API_KEY'
}

# API Endpoints
API_ENDPOINTS = {
    'openai': {
        'base_url': 'https://api.openai.com/v1',
        'completions': '/completions',
        'chat': '/chat/completions',
        'edits': '/edits'
    },
    'stable_diffusion': {
        'base_url': 'https://api.stability.ai/v1',
        'text2img': '/generation/stable-diffusion-v1-5/text-to-image',
        'img2img': '/generation/stable-diffusion-v1-5/image-to-image'
    },
    'elevenlabs': {
        'base_url': 'https://api.elevenlabs.io/v1',
        'text2speech': '/text-to-speech',
        'voices': '/voices'
    }
}

# API Settings
API_SETTINGS = {
    'openai': {
        'model': 'gpt-3.5-turbo',
        'settings': {
            'temperature': 0.7,
            'max_tokens': 1000,
            'top_p': 1.0,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        },
        'retry_settings': {
            'max_retries': 3,
            'retry_delay': 1,
            'timeout': 30
        }
    },
    'stable_diffusion': {
        'model': 'stable-diffusion-v1-5',
        'settings': {
            'steps': 30,
            'cfg_scale': 7.0,
            'width': 1024,
            'height': 1024,
            'samples': 1
        },
        'retry_settings': {
            'max_retries': 2,
            'retry_delay': 2,
            'timeout': 60
        }
    },
    'elevenlabs': {
        'model': 'eleven_multilingual_v1',
        'settings': {
            'stability': 0.5,
            'similarity_boost': 0.75,
            'style': 1.0,
            'use_speaker_boost': True
        },
        'retry_settings': {
            'max_retries': 3,
            'retry_delay': 1,
            'timeout': 30
        }
    }
}

# Rate Limits
RATE_LIMITS = {
    'openai': {
        'requests_per_minute': 60,
        'tokens_per_minute': 90000
    },
    'stable_diffusion': {
        'requests_per_minute': 30,
        'images_per_request': 4
    },
    'elevenlabs': {
        'characters_per_month': 10000,
        'requests_per_day': 100
    }
}

# Error Messages
API_ERRORS = {
    'openai': {
        'rate_limit': 'OpenAI API rate limit aşıldı. Lütfen biraz bekleyin.',
        'invalid_key': 'Geçersiz OpenAI API anahtarı.',
        'server_error': 'OpenAI sunucu hatası. Lütfen daha sonra tekrar deneyin.'
    },
    'stable_diffusion': {
        'rate_limit': 'Stable Diffusion API rate limit aşıldı. Lütfen biraz bekleyin.',
        'invalid_key': 'Geçersiz Stable Diffusion API anahtarı.',
        'server_error': 'Stable Diffusion sunucu hatası. Lütfen daha sonra tekrar deneyin.'
    },
    'elevenlabs': {
        'rate_limit': 'ElevenLabs API rate limit aşıldı. Lütfen biraz bekleyin.',
        'invalid_key': 'Geçersiz ElevenLabs API anahtarı.',
        'server_error': 'ElevenLabs sunucu hatası. Lütfen daha sonra tekrar deneyin.'
    }
}

# Cache Settings
CACHE_SETTINGS = {
    'openai': {
        'enable_cache': True,
        'cache_duration': 3600,  # 1 saat
        'max_cache_size': 1000   # maksimum önbellek girişi
    },
    'stable_diffusion': {
        'enable_cache': True,
        'cache_duration': 7200,  # 2 saat
        'max_cache_size': 500    # maksimum önbellek girişi
    },
    'elevenlabs': {
        'enable_cache': True,
        'cache_duration': 86400, # 24 saat
        'max_cache_size': 200    # maksimum önbellek girişi
    }
}
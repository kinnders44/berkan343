# video_config.py

# FFmpeg Ayarları
FFMPEG_SETTINGS = {
    # Video Codec Ayarları
    'video_codec': {
        'name': 'libx264',
        'preset': 'medium',
        'crf': 23  # Kalite ayarı (0-51, düşük=daha iyi)
    },
    
    # Audio Codec Ayarları
    'audio_codec': {
        'name': 'aac',
        'bitrate': '192k',
        'sample_rate': 44100
    },
    
    # Bitrate Ayarları
    'bitrates': {
        '720p': '2M',
        '1080p': '4M',
        '4K': '8M'
    },
    
    # Video Formatları
    'formats': {
        '9:16': {  # Stories, TikTok, Reels
            'width': 1080,
            'height': 1920,
            'aspect_ratio': '9:16'
        },
        '16:9': {  # YouTube, Standard
            'width': 1920,
            'height': 1080,
            'aspect_ratio': '16:9'
        },
        '1:1': {   # Instagram Post
            'width': 1080,
            'height': 1080,
            'aspect_ratio': '1:1'
        }
    },
    
    # FPS ve Frame Ayarları
    'frame_settings': {
        'fps': 30,
        'keyframe_interval': 60,  # Her 60 frame'de bir keyframe
    },
    
    # Geçiş Efektleri
    'transitions': {
        'fade': {
            'duration': 0.5,
            'type': 'fade_in_out'
        },
        'dissolve': {
            'duration': 0.7,
            'type': 'cross_dissolve'
        },
        'slide': {
            'duration': 0.6,
            'type': 'slide_left'
        }
    },
    
    # Watermark Ayarları
    'watermark': {
        'position': {
            'bottomright': {'x': 'W-w-20', 'y': 'H-h-20'},
            'bottomleft': {'x': '20', 'y': 'H-h-20'},
            'topright': {'x': 'W-w-20', 'y': '20'},
            'topleft': {'x': '20', 'y': '20'}
        },
        'default_position': 'bottomright',
        'padding': 20,
        'opacity': 0.8,
        'scale': 0.2  # Orijinal boyutun  'si
    },
    
    # Filtre Ayarları
    'filters': {
        'brightness': 1.0,
        'contrast': 1.0,
        'saturation': 1.0,
        'sharpness': 1.2
    },
    
    # Render Ayarları
    'render_settings': {
        'threads': 4,
        'priority': 'high',
        'temp_folder': 'temp_renders'
    }
}

# Video Kalite Presetleri
QUALITY_PRESETS = {
    'basic': {
        'resolution': '720p',
        'bitrate': FFMPEG_SETTINGS['bitrates']['720p'],
        'audio_quality': 'medium'
    },
    'pro': {
        'resolution': '1080p',
        'bitrate': FFMPEG_SETTINGS['bitrates']['1080p'],
        'audio_quality': 'high'
    },
    'premium': {
        'resolution': '4K',
        'bitrate': FFMPEG_SETTINGS['bitrates']['4K'],
        'audio_quality': 'ultra'
    }
}

# Video Export Formatları
EXPORT_FORMATS = {
    'mp4': {
        'container': 'mp4',
        'video_codec': 'libx264',
        'audio_codec': 'aac'
    },
    'webm': {
        'container': 'webm',
        'video_codec': 'libvpx-vp9',
        'audio_codec': 'libopus'
    },
    'mov': {
        'container': 'mov',
        'video_codec': 'prores',
        'audio_codec': 'pcm_s16le'
    }
}
"""
NANBAN AI - Voice Handler
Google Cloud Text-to-Speech Integration with Tamil voices
"""

import os
from google.cloud import texttospeech
import hashlib
import base64

class VoiceHandler:
    def __init__(self):
        # Initialize Google Cloud TTS client
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.enabled = True
        except Exception as e:
            print(f"Warning: Google Cloud TTS not configured: {e}")
            print("Voice features will be disabled. To enable:")
            print("1. Set up Google Cloud account")
            print("2. Enable Text-to-Speech API")
            print("3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            self.enabled = False
        
        # Voice mapping for different slangs
        self.voice_config = {
            'CHENNAI': {
                'name': 'ta-IN-Wavenet-A',  # Male, energetic
                'speaking_rate': 1.15,  # Faster (Chennai is fast-paced)
                'pitch': 1.0
            },
            'KOVAI': {
                'name': 'ta-IN-Wavenet-B',  # Male, softer
                'speaking_rate': 0.92,  # Slower (Kovai is calm)
                'pitch': 0.0
            },
            'MADURAI': {
                'name': 'ta-IN-Wavenet-A',  # Male, authoritative
                'speaking_rate': 1.0,  # Normal speed
                'pitch': -2.0  # Lower pitch (authority)
            },
            'NELLAI': {
                'name': 'ta-IN-Wavenet-A',  # Male, energetic
                'speaking_rate': 1.1,  # Slightly fast
                'pitch': 2.0  # Higher pitch (lively)
            },
            'EELAM': {
                'name': 'ta-IN-Wavenet-B',  # Male, gentle
                'speaking_rate': 0.95,  # Slightly slow
                'pitch': 0.0  # Normal pitch
            },
            'COMMON': {
                'name': 'ta-IN-Wavenet-A',  # Male, neutral
                'speaking_rate': 1.0,  # Normal
                'pitch': 0.0  # Normal
            }
        }
        
        # Persona modifiers
        self.persona_modifiers = {
            'JALIANA': {
                'pitch_adjust': 1.0,  # Slightly higher (energetic)
                'rate_adjust': 1.05  # Slightly faster
            },
            'AMAITHIYANA': {
                'pitch_adjust': -0.5,  # Slightly lower (calm)
                'rate_adjust': 0.92  # Slower (peaceful)
            },
            'THELIVANA': {
                'pitch_adjust': 0.0,  # Normal
                'rate_adjust': 1.0  # Normal (professional)
            },
            'VILAKKAMAANA': {
                'pitch_adjust': -1.0,  # Lower (teacher-like)
                'rate_adjust': 0.95  # Slightly slower (explanatory)
            }
        }
    
    def text_to_speech(self, text, slang='COMMON', persona='JALIANA'):
        """Convert text to speech with appropriate voice for slang and persona"""
        
        if not self.enabled:
            print("TTS disabled, returning None")
            return None
        
        try:
            # Get voice configuration for this slang
            voice_cfg = self.voice_config.get(slang, self.voice_config['COMMON'])
            persona_mod = self.persona_modifiers.get(persona, self.persona_modifiers['JALIANA'])
            
            # Clean text for TTS (remove emojis, keep Tamil and English)
            clean_text = self._clean_text_for_tts(text)
            
            # If text is very long, truncate for TTS (but keep full text in chat)
            if len(clean_text) > 500:
                clean_text = clean_text[:500] + "..."
            
            # Prepare SSML for more natural speech
            ssml_text = self._create_ssml(clean_text, voice_cfg, persona_mod)
            
            # Set up voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code="ta-IN",
                name=voice_cfg['name']
            )
            
            # Calculate final speaking rate and pitch
            final_rate = voice_cfg['speaking_rate'] * persona_mod['rate_adjust']
            final_pitch = voice_cfg['pitch'] + persona_mod['pitch_adjust']
            
            # Set up audio configuration
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=final_rate,
                pitch=final_pitch
            )
            
            # Synthesize speech
            synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
            
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Convert audio to base64 for easy transmission
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            # Return as data URL
            return f"data:audio/mp3;base64,{audio_base64}"
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def _clean_text_for_tts(self, text):
        """Remove emojis and clean text for TTS"""
        # Remove common emojis
        emoji_list = ['😄', '🔥', '😊', '😅', '🎉', '👏', '💪', '🚀', '⭐', '✨', '💯', '😂', '🤣', '😍', '🥰', '😎']
        cleaned = text
        for emoji in emoji_list:
            cleaned = cleaned.replace(emoji, '')
        
        # Clean up extra spaces
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def _create_ssml(self, text, voice_cfg, persona_mod):
        """Create SSML for more natural speech with pauses"""
        
        # Add natural pauses for better flow
        # Replace common punctuation with pauses
        ssml_text = text.replace('!', '<break time="300ms"/>')
        ssml_text = ssml_text.replace('?', '<break time="300ms"/>')
        ssml_text = ssml_text.replace('...', '<break time="500ms"/>')
        ssml_text = ssml_text.replace('.', '<break time="200ms"/>')
        ssml_text = ssml_text.replace(',', '<break time="150ms"/>')
        
        # Wrap in SSML speak tag
        ssml = f"""
        <speak>
            {ssml_text}
        </speak>
        """
        
        return ssml.strip()

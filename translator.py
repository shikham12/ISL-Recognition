# translator.py
import os
from gtts import gTTS
from playsound import playsound
import tempfile

# Translation dictionary for each gesture
TRANSLATIONS = {
    "hello": {
        "english": "Hello", "hindi": "नमस्ते", "gujarati": "નમસ્તે", "tamil": "வணக்கம்",
        "spanish": "Hola", "german": "Hallo"
    },
    "yes": {
        "english": "Yes", "hindi": "हाँ", "gujarati": "હા", "tamil": "ஆம்",
        "spanish": "Sí", "german": "Ja"
    },
    "goodbye": {
        "english": "Good Bye", "hindi": "अलविदा", "gujarati": "આવજો", "tamil": "விடைபெறுகிறேன்",
        "spanish": "adiós", "german": "Verabschiedung"
    },
    "thank you": {
        "english": "Thank you", "hindi": "धन्यवाद", "gujarati": "આભાર", "tamil": "நன்றி",
        "spanish": "Gracias", "german": "Danke"
    },
    "nice": {
        "english": "Nice", "hindi": "अच्छा", "gujarati": "સારું", "tamil": "நல்லது",
        "spanish": "Bonito", "german": "Schön"
    },
    "help": {
        "english": "Help", "hindi": "मदद", "gujarati": "મદદ", "tamil": "உதவி",
        "spanish": "Ayuda", "german": "Hilfe"
    }
}

def translate_gesture(gesture, language):
    gesture = gesture.lower()
    language = language.lower()
    return TRANSLATIONS.get(gesture, {}).get(language, "Translation not available")



def speak_translation(text, lang_code,out_path):
    tts = gTTS(text=text, lang=lang_code)
    #file_path = "temp_audio.mp3"  # Save in current directory
    tts.save(out_path)
    #playsound(file_path, block=False) # Play asynchronously
        # Add a small delay to allow playback to start before potential removal
        # This is a simple workaround; a more robust solution might be needed
        # if the audio gets cut off.
        # Adjust sleep time if needed based on audio length
        
# Map language names to gTTS codes
LANGUAGE_CODES = {
    "english": "en",
    "hindi": "hi",
    "gujarati": "gu",
    "tamil": "ta",
    "spanish": "es",
    "german": "de"
}

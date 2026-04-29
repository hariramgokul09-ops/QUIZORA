# textToSpeech.py
import pyttsx3
import threading

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine

def speak(text):
    def _s():
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_s, daemon=True).start()
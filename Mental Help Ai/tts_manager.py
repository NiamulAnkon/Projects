import pyttsx3
from setting_window import load_settings  # import your settings loader

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.apply_settings()

    def apply_settings(self):
        settings = load_settings()

        # Volume
        volume = settings.get("volume", 80) / 100
        self.engine.setProperty("volume", volume)

        # Speech Rate
        rate = settings.get("speech_rate", 100)
        self.engine.setProperty("rate", rate)

        # Voice (male/female depends on system voices)
        voices = self.engine.getProperty("voices")
        selected = settings.get("voice", "Male")

        if selected == "Male":
            self.engine.setProperty("voice", voices[0].id)
        elif selected == "Female" and len(voices) > 1:
            self.engine.setProperty("voice", voices[1].id)
        # Robotic/Natural would require mapping to available system voices
        # (we can fake this later with voice IDs)

    def speak(self, text: str):
        self.apply_settings()  # Re-apply in case user changed settings
        self.engine.say(text)
        self.engine.runAndWait()

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class MoodAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_mood(self, text: str) -> str:
        """
        Analyze mood from text using VADER sentiment scores.
        Returns: one of ['happy', 'sad', 'angry', 'neutral']
        """
        if not text.strip():
            return "neutral"

        scores = self.analyzer.polarity_scores(text)
        compound = scores["compound"]

        # Map compound score to moods
        if compound >= 0.6:
            return "happy"
        elif compound <= -0.6:
            # differentiate between sad & angry by checking negative intensity
            if "angry" in text.lower() or "furious" in text.lower() or "mad" in text.lower():
                return "angry"
            return "sad"
        elif -0.6 < compound < -0.2:
            return "sad"
        elif 0.2 < compound < 0.6:
            return "happy"
        else:
            return "neutral"
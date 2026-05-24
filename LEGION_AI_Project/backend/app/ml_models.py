"""
Machine learning models used in the MVP.

For financial anomaly detection we use an Isolation Forest trained on sample
spending data to flag unusual transactions.  For mood sentiment we use
NLTK's Vader sentiment analyser.  These models are simple and non‑clinical,
serving only as illustrative placeholders.  In production you would
replace them with validated models trained on appropriate datasets.
"""

from typing import List
import numpy as np
from sklearn.ensemble import IsolationForest

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
    # Ensure vader lexicon is available
    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon')
    _sentiment_analyzer = SentimentIntensityAnalyzer()
except Exception:
    _sentiment_analyzer = None


class SpendingAnomalyModel:
    """
    Anomaly detection model for spending behaviour using IsolationForest.
    The model is trained on historical amounts to determine what is "normal".
    """

    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_fitted = False

    def fit(self, amounts: List[float]):
        if len(amounts) < 10:
            # not enough data to train; set to trivial model
            self.is_fitted = False
            return
        X = np.array(amounts).reshape(-1, 1)
        self.model.fit(X)
        self.is_fitted = True

    def score(self, amount: float) -> float:
        """
        Returns an anomaly score in [0, 1], where values >0.6 indicate
        an outlier.
        """
        if not self.is_fitted:
            return 0.0
        score = -self.model.decision_function([[amount]])[0]  # higher means more anomalous
        # Scale between 0 and 1
        score_scaled = (score - self.model.offset_) / max(1e-5, abs(self.model.offset_))
        return float(max(0.0, min(1.0, score_scaled)))


def sentiment_score(text: str) -> float:
    """
    Compute sentiment polarity using Vader. Returns a number between -1 and 1.
    Positive scores indicate positive sentiment; negative indicate negative.
    If the analyser is unavailable the function returns 0.
    """
    if not _sentiment_analyzer:
        return 0.0
    scores = _sentiment_analyzer.polarity_scores(text)
    return scores.get('compound', 0.0)
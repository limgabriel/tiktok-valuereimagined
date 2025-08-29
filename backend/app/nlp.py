from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np
import math

_SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
# If bandwidth is tight, swap to distilbert sst2; keep API the same.

_sentiment = None

def init():
    global _sentiment
    if _sentiment is None:
        _sentiment = pipeline("sentiment-analysis", model=_SENTIMENT_MODEL, top_k=None)

def analyze_sentiment(comments):
    init()
    if not comments:
        return {"positive": 0.0, "neutral": 1.0, "negative": 0.0}, 0.0
    preds = _sentiment(comments)
    # Aggregate probabilities
    pos = neg = neu = 0.0
    for p in preds:
        # p like [{'label': 'positive', 'score':0.9}, ...]
        d = {x['label'].lower(): x['score'] for x in p}
        pos += d.get("positive", 0.0)
        neu += d.get("neutral", 0.0)
        neg += d.get("negative", 0.0)
    n = len(comments)
    return {"positive": pos/n, "neutral": neu/n, "negative": neg/n}, toxicity_heuristic(comments)

# extremely simple toxicity heuristic for POC
_TOXIC_WORDS = {"hate", "stupid", "idiot", "trash", "kill", "die", "racist"}

def toxicity_heuristic(comments):
    tokens = []
    foul = 0
    total = 0
    for c in comments:
        words = [w.strip(".,!?;:()[]{}").lower() for w in c.split()]
        total += max(1, len(words))
        tokens.extend(words)
        foul += sum(1 for w in words if w in _TOXIC_WORDS)
    tox = min(1.0, foul / (total or 1))
    return round(tox, 3)

# simple PPL: use character-level heuristic (no heavy LM download)
def pseudo_perplexity(text: str) -> float:
    if not text:
        return 100.0
    # lower variety + repetitive punctuation -> lower ppl (AI-ish)
    unique = len(set(text.split()))
    length = len(text.split())
    repet = sum(1 for i in range(1, len(text.split())) if text.split()[i]==text.split()[i-1])
    ratio = unique / (length or 1)
    ppl = 80 * (ratio) + 20 * (repet/(length or 1))
    return max(5.0, min(150.0, ppl))

def aigc_likelihood(text: str) -> (float, float):
    ppl = pseudo_perplexity(text)
    # map ppl (low -> high AI prob)
    # heuristic: ppl<25 -> 0.8..1; ppl>60 -> 0..0.3
    if ppl <= 25:
        prob = 0.9
    elif ppl >= 60:
        prob = 0.2
    else:
        # linear in between
        prob = 0.9 - (ppl-25) * (0.7/35.0)
    return round(max(0.0, min(1.0, prob)), 3), round(ppl, 2)

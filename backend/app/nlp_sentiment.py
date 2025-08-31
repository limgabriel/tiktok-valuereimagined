import argparse
import json
import math
import statistics
import os
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import time

load_dotenv()
APIFY_TOKEN= os.getenv("APIFY_TOKEN")
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")
LIMIT = 100

def fetch_comments(url, actor_id=APIFY_ACTOR_ID, token=APIFY_TOKEN, limit=LIMIT):
    def _apify_run_actor(actor_id: str, payload: dict, token: str):
        url = f"https://api.apify.com/v2/acts/{actor_id}/runs"
        r = requests.post(url, params={"token": token}, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["data"]

    def _apify_wait_for_run(run_id: str, token: str, timeout_s: int = 240) -> dict:
        """Polls Apify until the run finishes; returns the final run JSON."""
        url = f"https://api.apify.com/v2/actor-runs/{run_id}"
        deadline = time.time() + timeout_s
        while True:
            r = requests.get(url, params={"token": token}, timeout=20)
            r.raise_for_status()
            data = r.json()["data"]
            status = data["status"]
            if status in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"):
                return data
            if time.time() > deadline:
                raise TimeoutError(f"Apify run timed out (status={status})")
            time.sleep(2)

    def _apify_fetch_items(dataset_id: str, token: str, limit: int | None = None) -> list:
        url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
        params = {"token": token, "format": "json", "clean": "true"}
        if limit is not None:
            params["limit"] = limit
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        return r.json()

    def _extract_comment_texts(items: list) -> list[str]:
        """Extracts plain comment text from dataset items (handles common field names)."""
        comments = []
        for it in items:
            txt = (
                it.get("text")
                or it.get("comment")
                or it.get("content")
                or it.get("commentText")
            )
            if isinstance(txt, str) and txt.strip():
                comments.append(txt.strip())
        return comments

    actor_input = {
        "postURLs": [url],
        "commentsPerPost": limit
    }

    run = _apify_run_actor(actor_id, actor_input, token)
    run = _apify_wait_for_run(run["id"], token, timeout_s=240)

    if run["status"] != "SUCCEEDED":
        raise RuntimeError(f"Run ended with status {run['status']}")

    dataset_id = run.get("defaultDatasetId")
    if not dataset_id:
        raise RuntimeError("No defaultDatasetId on the run; nothing to fetch.")

    items = _apify_fetch_items(dataset_id, token)  
    comments = _extract_comment_texts(items)
    print(f"Fetched {len(comments)} comments. Sample:")
    print("\n".join(comments[:5]))
    return comments

def sentiment_to_pos_score(label_scores: List[Dict[str, float]]) -> float:
    """
    Map model outputs to [0,1] positivity.
    Model labels: 'negative', 'neutral', 'positive'
    We'll use: score = 1*P(positive) + 0.5*P(neutral) + 0*P(negative)
    """
    probs = {d['label'].lower(): d['score'] for d in label_scores}
    p_pos = probs.get('positive', 0.0)
    p_neu = probs.get('neutral', 0.0)
    p_neg = probs.get('negative', 0.0)
    # Safety re-normalization
    z = max(p_pos + p_neu + p_neg, 1e-9)
    p_pos, p_neu, p_neg = p_pos/z, p_neu/z, p_neg/z
    return float(1.0 * p_pos + 0.5 * p_neu + 0.0 * p_neg)

def perspective_toxicity_score(text: str) -> Optional[float]:
    """
    Returns toxicity in [0,1] using Perspective API.
    If no API key is present or request fails, returns None.
    """
    if not PERSPECTIVE_API_KEY:
        return None
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True
    }
    try:
        r = requests.post(url, params={"key": PERSPECTIVE_API_KEY}, json=data, timeout=8)
        r.raise_for_status()
        resp = r.json()
        score = resp["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        return float(score)  # 0..1 where 1 = very toxic
    except Exception:
        return None
    
# Import Huggingface model
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

def build_sentiment_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)
    return TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)


def get_comments_score(comments: List[str]):
    agg_scores = {
        'positivity_scores': [],
        'toxicity_scores': [],
    }
    sentiment_pipe = build_sentiment_pipeline()

    for text in tqdm(comments, desc="Scoring comments"):
        # Run sentiment
        out = sentiment_pipe(text, truncation=True)[0]
        pos = sentiment_to_pos_score(out)
        tox = perspective_toxicity_score(text)

        agg_scores['positivity_scores'].append(pos)
        if tox is not None:
            agg_scores['toxicity_scores'].append(tox)

    avg_positivity = statistics.mean(agg_scores['positivity_scores']) if agg_scores['toxicity_scores'] else 0.0
    avg_toxicity = statistics.mean(agg_scores['toxicity_scores']) if agg_scores['toxicity_scores'] else 0.0

    return avg_positivity, avg_toxicity








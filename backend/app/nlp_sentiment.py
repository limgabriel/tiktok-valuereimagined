import os
import time
import statistics
from typing import List, Dict, Optional
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")
LIMIT = 100

# ------------------- APIFY COMMENTS FETCHING -------------------

def fetch_comments(url: str, actor_id: str = APIFY_ACTOR_ID, token: str = APIFY_TOKEN, limit: int = LIMIT) -> List[str]:
    """Fetch comments from TikTok using Apify Actor."""
    
    def _apify_run_actor(actor_id: str, payload: dict, token: str):
        r = requests.post(f"https://api.apify.com/v2/acts/{actor_id}/runs",
                          params={"token": token}, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["data"]

    def _apify_wait_for_run(run_id: str, token: str, timeout_s: int = 240) -> dict:
        url = f"https://api.apify.com/v2/actor-runs/{run_id}"
        deadline = time.time() + timeout_s
        while True:
            r = requests.get(url, params={"token": token}, timeout=20)
            r.raise_for_status()
            data = r.json()["data"]
            if data["status"] in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"):
                return data
            if time.time() > deadline:
                raise TimeoutError(f"Apify run timed out (status={data['status']})")
            time.sleep(2)

    def _apify_fetch_items(dataset_id: str, token: str, limit: Optional[int] = None) -> list:
        params = {"token": token, "format": "json", "clean": "true"}
        if limit is not None:
            params["limit"] = limit
        r = requests.get(f"https://api.apify.com/v2/datasets/{dataset_id}/items",
                         params=params, timeout=60)
        r.raise_for_status()
        return r.json()

    def _extract_comment_texts(items: list) -> list[str]:
        comments = []
        for it in items:
            txt = it.get("text") or it.get("comment") or it.get("content") or it.get("commentText")
            if isinstance(txt, str) and txt.strip():
                comments.append(txt.strip())
        return comments

    actor_input = {"postURLs": [url], "commentsPerPost": limit}
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

# ------------------- SENTIMENT & TOXICITY -------------------

SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Load tokenizer and model once (Railway-friendly)
print("[DEBUG] Loading Hugging Face sentiment model...")
tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)
sentiment_pipe = TextClassificationPipeline(
    model=model, tokenizer=tokenizer, return_all_scores=True
)
print("[DEBUG] Model loaded!")

def sentiment_to_pos_score(label_scores: List[Dict[str, float]]) -> float:
    """Map sentiment output to [0,1] positivity score."""
    probs = {d['label'].lower(): d['score'] for d in label_scores}
    p_pos = probs.get('positive', 0.0)
    p_neu = probs.get('neutral', 0.0)
    p_neg = probs.get('negative', 0.0)
    z = max(p_pos + p_neu + p_neg, 1e-9)
    p_pos, p_neu, p_neg = p_pos/z, p_neu/z, p_neg/z
    return float(1.0 * p_pos + 0.5 * p_neu + 0.0 * p_neg)

def perspective_toxicity_score_safe(text: str) -> Optional[float]:
    """Returns toxicity in [0,1] using Perspective API, None if fails or key missing."""
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
        return float(r.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
    except Exception:
        return None

def get_comments_score(comments: List[str], max_workers: int = 4, batch_size: int = 32):
    """
    Compute positivity + toxicity scores for a list of comments.
    Hugging Face model used for sentiment (batched), toxicity is parallelized.
    """
    agg_scores = {"positivity_scores": [], "toxicity_scores": []}

    # --- Batch sentiment scoring ---
    for i in tqdm(range(0, len(comments), batch_size), desc="Analyzing positivity (HF)"):
        batch = comments[i:i+batch_size]
        sentiment_outputs = sentiment_pipe(batch, truncation=True)
        for out in sentiment_outputs:
            agg_scores["positivity_scores"].append(sentiment_to_pos_score(out))

    # --- Parallelized Perspective API ---
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(perspective_toxicity_score_safe, c): c for c in comments}
        for future in tqdm(as_completed(futures), total=len(comments), desc="Toxicity"):
            tox = future.result()
            if tox is not None:
                agg_scores["toxicity_scores"].append(tox)

    avg_positivity = statistics.mean(agg_scores["positivity_scores"]) if agg_scores["positivity_scores"] else 0.0
    avg_toxicity = statistics.mean(agg_scores["toxicity_scores"]) if agg_scores["toxicity_scores"] else 0.0

    return avg_positivity, avg_toxicity
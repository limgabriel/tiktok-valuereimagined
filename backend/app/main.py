from fastapi import FastAPI
from .schemas import *
from .nlp import analyze_sentiment, aigc_likelihood
from .scoring import composite_score, rationale_text
from .storage import put, get

app = FastAPI(title="Creator Value Score API")

@app.post("/analyze/comments", response_model=AnalyzeCommentsResponse)
def analyze_comments(req: AnalyzeCommentsRequest):
    sentiment, tox = analyze_sentiment(req.comments)
    # crude engagement score ~ comment volume (normalized)
    eng = min(1.0, len(req.comments) / 50.0)
    top_terms = sorted(set(" ".join(req.comments).lower().split()))[:10]
    payload = {"sentiment": sentiment, "toxicity": tox, "engagement_score": eng, "top_terms": top_terms}
    put(req.video_id+"_comments", payload)
    return payload

@app.post("/analyze/content", response_model=AnalyzeContentResponse)
def analyze_content(req: AnalyzeContentRequest):
    prob, ppl = aigc_likelihood(req.transcript or "")
    payload = {"aigc_likelihood": prob, "perplexity": ppl}
    put(req.video_id+"_content", payload)
    return payload


@app.get("/creator_value_score/{video_id}", response_model=CreatorValueScoreResponse)
def creator_value_score(video_id: str):

    # Try to fetch stored analysis
    # c = get(video_id+"_comments") 
    # t = get(video_id+"_content")
    c, t = None, None # assume no in-mem cache for POC

    # If comments not stored, analyze placeholder comments (or fetch real comments)
    if not c:
        # For demo: assume empty comments
        dummy_comments = []
        sentiment, tox = analyze_sentiment(dummy_comments)
        eng = 0.0
        c = {"sentiment": sentiment, "toxicity": tox, "engagement_score": eng}
        put(video_id+"_comments", c)

    # If content not stored, analyze placeholder transcript
    if not t:
        # For demo: assume empty transcript
        prob, ppl = aigc_likelihood("")
        t = {"aigc_likelihood": prob, "perplexity": ppl}
        put(video_id+"_content", t)

    # Compute composite score
    score = composite_score(c["sentiment"], c.get("toxicity",0.0), t["aigc_likelihood"])

    return {
        "video_id": video_id,
        "sentiment": c["sentiment"],
        "toxicity": c.get("toxicity", 0.0),
        "engagement_score": c.get("engagement_score", 0.0),
        "aigc_likelihood": t["aigc_likelihood"],
        "composite_score": score,
        "rationale": rationale_text(
            c["sentiment"],
            c.get("toxicity",0.0),
            t["aigc_likelihood"],
            score
        )
    }
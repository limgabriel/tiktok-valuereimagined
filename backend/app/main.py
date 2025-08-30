from fastapi import FastAPI, HTTPException
from .schemas import *
from .analysis import *

app = FastAPI(title="TikTok Reward Analysis API")

# ---------------------------
# Main Endpoint
# ---------------------------
@app.post("/analyse_tiktok", response_model=TikTokResponse)
async def analyse_tiktok_endpoint(request: TikTokRequest):
    result = await analyse_tiktok_video(request.video_url)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

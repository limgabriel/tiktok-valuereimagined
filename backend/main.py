import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas import TikTokRequest, TikTokResponse
from backend.app.analysis import analyse_tiktok_video

logger = logging.getLogger(__name__)

app = FastAPI(title="TikTok Reward Analysis API")

# Allow your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://front-end-production-af24.up.railway.app"  # your Railway frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Main Endpoint
# ---------------------------
@app.post("/analyse_tiktok", response_model=TikTokResponse)
async def analyse_tiktok_endpoint(request: TikTokRequest):
    logger.info("DEBUG: incoming request %s", request.dict())
    result = await analyse_tiktok_video(request.video_url)
    logger.info("DEBUG: function returned %s", result)
    if result.get("error"):
        logger.error("DEBUG: raising 400 with %s", result["error"])
        raise HTTPException(status_code=400, detail=result["error"])
    return result

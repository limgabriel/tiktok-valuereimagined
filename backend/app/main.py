from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from analysis import *

app = FastAPI(title="TikTok Reward Analysis API")
# Allow your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://front-end-production-af24.up.railway.app"],  # your React app
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, OPTIONS, etc.
    allow_headers=["*"],  # allow Content-Type, etc.
)

# ---------------------------
# Main Endpoint
# ---------------------------
@app.post("/analyse_tiktok", response_model=TikTokResponse)
async def analyse_tiktok_endpoint(request: TikTokRequest):
    result = await analyse_tiktok_video(request.video_url)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

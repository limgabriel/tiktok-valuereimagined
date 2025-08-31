import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas import TikTokRequest, TikTokResponse
from backend.app.analysis import analyse_tiktok_video

# ---------------------------
# Logging setup
# ---------------------------
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG level to see detailed logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------
# FastAPI setup
# ---------------------------
app = FastAPI(title="TikTok Reward Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://front-end-production-af24.up.railway.app"
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
    try:
        logger.debug("Incoming request: %s", request.dict())
        
        # Call analysis function
        result = await analyse_tiktok_video(request.video_url)
        logger.debug("Analysis result: %s", result)
        
        # Check for internal errors
        if result.get("error"):
            logger.error("Error detected in analysis: %s", result["error"])
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result

    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise

    except Exception as e:
        # Catch-all for unexpected errors
        logger.error("Unhandled exception during analysis: %s", str(e))
        logger.error("Stack trace:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

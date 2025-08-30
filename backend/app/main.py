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
    print("DEBUG: incoming request", request.dict())
    result = await analyse_tiktok_video(request.video_url)
    print("DEBUG: function returned", result)
    if result.get("error"):
        print("DEBUG: raising 400 with", result["error"])
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.on_event("startup")
async def startup_event():
    browser_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/app/playwright-browsers")
    chromium_path = os.path.join(browser_path, "chromium-1187")
    if not os.path.exists(chromium_path):
        logger.info(f"Playwright browsers not found at {browser_path}. Installing...")
        try:
            os.makedirs(browser_path, exist_ok=True)
            subprocess.run(["chmod", "-R", "777", browser_path], check=True)
            subprocess.run(
                ["python", "-m", "playwright", "install", "--with-deps"],
                env={**os.environ, "PLAYWRIGHT_BROWSERS_PATH": browser_path},
                check=True,
            )
            logger.info("Playwright browsers installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install Playwright browsers: {e}")
            raise RuntimeError("Playwright browser installation failed")
    else:
        logger.info(f"Playwright browsers found at {browser_path}.")
import os
import uvicorn

if __name__ == "__main__":
    # Get PORT from environment (Railway sets this)
    port = int(os.environ.get("PORT", 8000))  # default 8000 for local dev
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port)
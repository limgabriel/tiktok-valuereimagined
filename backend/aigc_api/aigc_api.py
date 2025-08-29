import os
import shutil

from fastapi import FastAPI, Form, UploadFile, File
from tests.test_comments import video_id

from aigc import basic_example
from getTiktokApi import getJpgFromTTlink
import asyncio

app = FastAPI(title="Reality Defender API")

@app.post("/analyze-image/")
async def analyze_image(tiktok_link: str = Form(...)):
    """
    Analyze a TikTok video thumbnail using Reality Defender.
    Requires a TikTok link.
    """
    # Download the thumbnail from the TikTok link
    file_path, video_info = await getJpgFromTTlink(tiktok_link)
    print(file_path)
    # Run Reality Defender analysis
    result = await basic_example(file_path)
    result |= video_info
    result["filepath"] = file_path
    return result



UPLOAD_DIR = "sampleImages"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.post("/upload/")
async def save_file(file: UploadFile = File(...)):
    # Check MIME type
    if not file.content_type.startswith("image/"):
        return {"error": "Only image files are allowed."}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = await basic_example(file_path)
    result["filepath"] = file_path
    return result
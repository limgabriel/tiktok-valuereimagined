import asyncio
import json

import requests
from TikTokApi import TikTokApi

# Replace with your TikTok video ID
# VIDEO_URL = "https://www.tiktok.com/@azulacinta/video/7543089876946652436"

import asyncio
import requests
from TikTokApi import TikTokApi
from pathlib import Path
import re

async def getJpgFromTTlink(video_url):
    # Initialize TikTokApi
    api = TikTokApi()
    await api.create_sessions()

    # Get video object
    video = api.video(url=video_url)
    video_info = await video.info()  # is HTML request, so avoid using this too much
    duration = video_info["video"]["duration"]
    video_info = video_info["statsV2"]
    video_info["duration"] = duration


    # Fetch metadata (thumbnail, etc.)
    data = await video.info()  # async call
    cover_url = data["video"]["cover"]
    # Prepare safe file path
    name = video_url.split("www.tiktok.com/")[1]
    safe_name = re.sub(r"[\\/]", "_", name)  # replace slashes with underscores
    folder = Path("sampleImages")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"{safe_name}.jpg"

    # Download and save thumbnail
    img_data = requests.get(cover_url).content
    file_path.write_bytes(img_data)
    print(f"Thumbnail saved to: {file_path}")
    return file_path, video_info

if __name__ == "__main__":
    video_url= "https://www.tiktok.com/@azulacinta/video/7543089876946652436"
    asyncio.run(getJpgFromTTlink(video_url=video_url))

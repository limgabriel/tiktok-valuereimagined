import os
from pathlib import Path
import re

from TikTokApi import TikTokApi
from dotenv import load_dotenv
from realitydefender import RealityDefender, RealityDefenderError
import requests

from typing import Dict, Any
from backend.app.nlp_sentiment import get_comments_score, fetch_comments
from playwright.async_api import async_playwright
import asyncio


load_dotenv()

# ----- Utility Functions -----

async def fetch_tiktok_info(video_url: str):
    """Fetch TikTok video metadata & thumbnail."""
    api = TikTokApi()
    await api.create_sessions()

    video = api.video(url=video_url)
    video_info = await video.info()
    if not video_info or "video" not in video_info:
        raise ValueError("Failed to fetch TikTok video info.")

    duration = video_info["video"]["duration"]
    stats = video_info.get("statsV2", {}) or video_info.get("stats", {}) 
    stats["duration"] = duration
    stats['location'] = video_info.get("locationCreated", '')


    # Thumbnail
    cover_url = video_info["video"].get("cover")
    if not cover_url:
        raise ValueError("Thumbnail not found in TikTok video data.")

    # Save thumbnail locally
    safe_name = re.sub(r"[\\/]", "_", video_url.split("www.tiktok.com/")[1])
    folder = Path("/tmp/tt_thumbnails")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"{safe_name}.jpg"

    try:
        img_data = requests.get(cover_url, timeout=10).content
        file_path.write_bytes(img_data)
    except Exception as e:
        raise RuntimeError(f"Failed to download thumbnail: {str(e)}")

    return file_path, stats

async def run_reality_defender(file_path: Path) -> Dict[str, Any]:
    """Send thumbnail to Reality Defender API."""
    api_key = os.environ.get("REALITY_DEFENDER_API_KEY")
    if not api_key:
        raise EnvironmentError("REALITY_DEFENDER_API_KEY not set in environment.")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    client = RealityDefender(api_key=api_key)
    try:
        upload_result = await client.upload(file_path=file_path)
        request_id = upload_result.get("request_id")
        if not request_id:
            raise RuntimeError("Reality Defender upload failed (no request_id).")

        result = await client.get_result(request_id)
        return result

    except RealityDefenderError as e:
        raise RuntimeError(f"RealityDefender API error: {e.message} (Code: {e.code})")
    except Exception as e:
        raise RuntimeError(f"Unexpected RealityDefender error: {str(e)}")


async def analyse_tiktok_video(tt_link: str) -> Dict[str, Any]:
    try:
        # 1. Get thumbnail + local path using TikTokApi
        file_path, stats = await fetch_tiktok_info(tt_link)


        # 2. Run AIGC check on the downloaded thumbnail
        aigc_result = await run_reality_defender(file_path)

        # 3 Fetch comments asynchronously (wrap blocking fetch_comments)
        try:
            tt_comments = await asyncio.to_thread(fetch_comments, tt_link)
        except Exception as e:
            tt_comments = []
            print(f"[WARN] Failed to fetch comments: {e}")

        # 4 Safe numeric conversions
        def safe_float(x, default=0.0):
            try:
                return float(x.replace(",", "")) if isinstance(x, str) else float(x)
            except:
                return default

        views = safe_float(stats.get("playCount", 1), 1)
        likes = safe_float(stats.get("diggCount", 0))
        shares = safe_float(stats.get("shareCount", 0))
        comments = safe_float(stats.get("commentCount", 0))
        collect = safe_float(stats.get("collectCount", 0))

        # 4. Engagement Index (EVI)
        EVI = (
            0.1 * likes / views
            + 0.4 * shares / views
            + 0.3 * comments / views
            + 0.2 * collect / views
        )

        # 5. Rbase
        ad_revenue = 0.5
        gifted_stickers = 0.5
        Rbase = ad_revenue + gifted_stickers + EVI

        # 6. Mquality
        positivity_rate, toxicity_rate = get_comments_score(tt_comments)
        Mquality = 0.5 * positivity_rate + 0.5 * (1 - toxicity_rate)

        # 7. Mintegrity
        prob_aigc = aigc_result.get("score", 0)
        Mintegrity = 1 - 0.25 * min(1, prob_aigc)

        # 8. Bmission
        _TARGET_COUNTRIES = ["BR", "IN", "ZA"]
        _SMALL_CREATOR_THRESHOLD = 10000
        author = stats.get("author", {})
        small_creator = author.get("followerCount", 0) < _SMALL_CREATOR_THRESHOLD
        underrepresented_country = stats.get("location") in _TARGET_COUNTRIES
        Bmission = 1
        Bmission *= 1 + 0.1 * small_creator
        Bmission *= 1 + 0.1 * underrepresented_country

        # 9. Reward
        reward = Rbase * Mquality * Mintegrity * Bmission

        return {
            "video_url": tt_link,
            "reward_score": reward,
            "thumbnail": {"local_path": str(file_path), "url": stats.get("cover", "")},
            "video_stats": stats,
            "engagement_index": {
                "EVI": EVI,
                "components": {
                    "likes_ratio": likes / views,
                    "shares_ratio": shares / views,
                    "comments_ratio": comments / views,
                    "collect_ratio": collect / views,
                },
            },
            "content_quality": {
                "positivity_rate": positivity_rate,
                "toxicity_rate": toxicity_rate,
                "Mquality": Mquality,
            },
            "aigc_integrity": {
                "probability_aigc": prob_aigc,
                "Mintegrity": Mintegrity,
                "analysis_detail": aigc_result,
            },
            "mission_bonus": {
                "small_creator": small_creator,
                "underrepresented_country": underrepresented_country,
                "Bmission": Bmission,
            },
            "error": None,
        }

    except Exception as e:
        return {
            "video_url": tt_link,
            "reward_score": 0.0,
            "thumbnail": {"local_path": "", "url": ""},
            "video_stats": {},
            "engagement_index": {"EVI": 0.0, "components": {"likes_ratio": 0.0, "shares_ratio": 0.0, "comments_ratio": 0.0, "collect_ratio": 0.0}},
            "content_quality": {"positivity_rate": 0.0, "toxicity_rate": 0.0, "Mquality": 0.0},
            "aigc_integrity": {"probability_aigc": 0.0, "Mintegrity": 1.0, "analysis_detail": {}},
            "mission_bonus": {"small_creator": False, "underrepresented_country": False, "Bmission": 1.0},
            "error": str(e),
        }
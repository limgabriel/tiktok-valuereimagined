from pydantic import BaseModel
from typing import List, Dict, Optional
from typing import Optional, Dict, Any
from pydantic import BaseModel

# ---------------------------
# Request schema
# ---------------------------
class TikTokRequest(BaseModel):
    video_url: str

# ---------------------------
# Response schema
# ---------------------------
class ThumbnailInfo(BaseModel):
    local_path: str
    url: Optional[str] = None


class EngagementComponents(BaseModel):
    likes_ratio: float
    shares_ratio: float
    comments_ratio: float
    collect_ratio: float


class EngagementIndex(BaseModel):
    EVI: float
    components: EngagementComponents


class ContentQuality(BaseModel):
    positivity_rate: float
    toxicity_rate: float
    Mquality: float


class AIGCIntegrity(BaseModel):
    probability_aigc: float
    Mintegrity: float
    analysis_detail: Dict[str, Any]


class MissionBonus(BaseModel):
    small_creator: bool
    underrepresented_country: bool
    Bmission: float


class TikTokResponse(BaseModel):
    video_url: str
    reward_score: float
    thumbnail: ThumbnailInfo
    video_stats: Dict[str, Any]
    engagement_index: EngagementIndex
    content_quality: ContentQuality
    aigc_integrity: AIGCIntegrity
    mission_bonus: MissionBonus
    error: Optional[str] = None

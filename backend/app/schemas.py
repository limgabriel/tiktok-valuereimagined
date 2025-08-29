from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# Comment Section Analysis Request
class AnalyzeCommentsRequest(BaseModel):
    video_id: str
    comments: List[str] = Field(default_factory=list)

# Comment Section Analysis Response
class AnalyzeCommentsResponse(BaseModel):
    sentiment: Dict[str, float]
    toxicity: float
    engagement_score: float
    top_terms: List[str]

# AIGC Score Request
class AnalyzeContentRequest(BaseModel):
    video_id: str
    transcript: Optional[str] = ""

# AIGC Score Response
class AnalyzeContentResponse(BaseModel):
    aigc_likelihood: float
    perplexity: float

# Final Value Score Response
class CreatorValueScoreResponse(BaseModel):
    video_id: str
    sentiment: Dict[str, float]
    toxicity: float
    aigc_likelihood: float
    composite_score: float
    rationale: str

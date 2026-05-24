import pydantic
from pydantic import BaseModel, HttpUrl, Field
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScrapedPage:
    url: str
    raw_html: str
    # fetched_at: datetime = 
    status_code: int 
    
class ScrapeRequest(BaseModel):
    list_urls: list[HttpUrl] = Field(..., min_length=1, max_length=10)
    timeout: int
    max_words_per_page: int = Field(default=500, ge=100, le=2000)

class SummaryResult(BaseModel):
    url: str
    summary: str
    word_count: int
    duration_ms : int








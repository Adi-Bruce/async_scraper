from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


@dataclass
class ScrapedPage:
    url: str
    raw_html: str
    status_code: int
    fetched_at: datetime = field(default_factory=datetime.utcnow)
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status_code == 200


@dataclass
class ExtractedText:
    url: str
    text: str
    word_count: int
    truncated: bool = False


class ScrapeRequest(BaseModel):
    urls: list[HttpUrl] = Field(..., min_length=1, max_length=10)
    timeout_seconds: float = Field(default=10.0, ge=1.0, le=30.0)
    max_words_per_page: int = Field(default=500, ge=100, le=2000)


class SummaryResult(BaseModel):
    url: str
    summary: str | None
    word_count: int
    duration_ms: int
    status_code: int
    error: str | None = None


class SummarizeResponse(BaseModel):
    results: list[SummaryResult]
    total_urls: int
    successful: int
    failed: int
    total_duration_ms: int
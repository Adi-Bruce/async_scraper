from models import ScrapedPage,ExtractedText
import asyncio
import httpx
import time
from contextlib import asynccontextmanager
from models import MyHTMLParser

async def fetch(url: str, client: httpx.AsyncClient) -> ScrapedPage:
    try:
        response = await client.get(url)
        return ScrapedPage(
            url=url,
            raw_html=response.text,
            status_code=response.status_code,
        )
    except httpx.TimeoutException:
        return ScrapedPage(url=url, raw_html="", status_code=0, error="timeout")
    except httpx.RequestError as e:
        return ScrapedPage(url=url, raw_html="", status_code=0, error=str(e))


async def fetch_all(urls: list[str], timeout_seconds: int):
    async with httpx.AsyncClient(timeout=timeout_seconds) as cli:
        results = await asyncio.gather(
            *[fetch(url, cli) for url in urls],
        )
        return results

@asynccontextmanager
async def timer(label: str):
    t = time.perf_counter()
    result = {"elapsed_time":0.0}
    try:
        yield result
    finally:
        elapsed = (time.perf_counter() - t) * 1000
        result["elapsed_time"]=elapsed
        print(f"{label}: {result['elapsed_ms']:.1f}ms")


def extract_text(page: ScrapedPage, max_words: int = 500) -> ExtractedText:
    parser = MyHTMLParser()
    parser.feed(page.raw_html)
    text = parser.get_shi()

    words = text.split()
    truncated = False

    if len(words) > max_words:
        words = words[:max_words]
        truncated = True

    return ExtractedText(
        url=page.url,
        text=" ".join(words),
        word_count=len(words),
        truncated=truncated,
    )
from models import ScrapedPage
import asyncio
import httpx


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
            return_exceptions=True
        )
        return results

    
async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get()
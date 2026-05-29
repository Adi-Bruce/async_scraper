from models import ScrapedPage
import asyncio
import httpx


def fetch(url: str, client: httpx.AsnycClient)-> ScrapedPage:
    

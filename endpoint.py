from fastapi import FastAPI
from models import ScrapeRequest, SummarizeResponse, SummaryResult
from fetcher_cmanager import extract_text,fetch_all
import asyncio

app = FastAPI()

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: ScrapeRequest):
   
    pass
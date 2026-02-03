from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional
import os
import asyncio
from urllib.parse import urlparse
from dotenv import load_dotenv

from scraper import SocialScraper
from ai_engine import AIEngine

load_dotenv()

app = FastAPI(title="PulseTag API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    original_text: str
    hashtags: Dict[str, List[str]]

scraper = SocialScraper()
ai_engine = AIEngine()

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_post(request: AnalyzeRequest):
    try:
        # Validate URL to prevent SSRF
        parsed_url = urlparse(str(request.url))
        allowed_domains = ["linkedin.com", "twitter.com", "x.com"]
        
        if parsed_url.netloc not in allowed_domains:
            raise HTTPException(
                status_code=400,
                detail=f"URL domain not allowed. Only {', '.join(allowed_domains)} are supported."
            )
        
        # Extract text from the social media post
        text_content = await scraper.extract_text(request.url)
        
        if not text_content:
            # Provide more specific error message
            if "linkedin.com" in request.url:
                raise HTTPException(
                    status_code=400, 
                    detail="Could not extract text from LinkedIn. LinkedIn may require authentication. Please try with a public post or a different platform."
                )
            elif "twitter.com" in request.url or "x.com" in request.url:
                # Check if it's a profile URL
                if "/status/" not in request.url:
                    raise HTTPException(
                        status_code=400,
                        detail="This appears to be a Twitter profile URL. Please provide a URL to a specific tweet. Click on the tweet and copy that URL instead."
                    )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Could not extract text from this X/Tweet. Please ensure the tweet is public and accessible."
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract text from the provided URL. Please ensure it's a valid and accessible web page."
                )
        
        # Generate hashtags using AI
        hashtags = await ai_engine.analyze_post(text_content)
        
        return AnalyzeResponse(
            original_text=text_content,
            hashtags=hashtags
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

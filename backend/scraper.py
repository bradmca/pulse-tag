from playwright.async_api import async_playwright, BrowserContext, Page
from bs4 import BeautifulSoup
import asyncio
import random
from urllib.parse import urlparse
import os
from typing import Optional

class SocialScraper:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.linkedin_cookies = os.getenv("LINKEDIN_COOKIES", "")
    
    async def extract_text(self, url: str) -> Optional[str]:
        """Extract text content from a social media post URL."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.user_agent)
                
                # Add LinkedIn cookies if available
                if "linkedin.com" in url and self.linkedin_cookies:
                    await self._add_cookies(context, self.linkedin_cookies, "linkedin.com")
                
                page = await context.new_page()
                
                # Add random delay to avoid bot detection
                await asyncio.sleep(random.uniform(1, 3))
                
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # Wait a bit more for dynamic content
                await asyncio.sleep(2)
                
                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                text = None
                if "linkedin.com" in url:
                    text = self._extract_linkedin_text(soup)
                elif "twitter.com" in url or "x.com" in url:
                    text = self._extract_twitter_text(soup)
                else:
                    # For non-social media URLs, try to extract general content
                    text = self._extract_general_text(soup)
                
                await browser.close()
                return text
                
        except Exception as e:
            print(f"Error extracting text from {url}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_linkedin_text(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract text from LinkedIn post."""
        # Try multiple selectors for LinkedIn posts
        selectors = [
            'article[data-id] .feed-shared-text__text',
            '.feed-shared-update-v2__description',
            '[data-test-id="main-feed-activity-card"] .feed-shared-text',
            'article .break-words',
            '.feed-shared-text'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Fallback: look for any article with substantial text
        articles = soup.find_all('article')
        for article in articles:
            text = article.get_text(strip=True)
            if len(text) > 50:  # Only return if it's substantial
                return text
        
        return None
    
    def _extract_twitter_text(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract text from Twitter/X post."""
        # Check if it's a profile page
        if soup.find('div', {'data-testid': 'profileHeader'}):
            return "This appears to be a Twitter profile page, not a specific tweet. Please provide a URL to an individual tweet."
        
        # Try multiple selectors for Twitter posts
        selectors = [
            '[data-testid="tweetText"]',
            '.tweet-text',
            '[data-test-id="tweet"]',
            '.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1kbdv8c'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Fallback: look for div with tweet-like structure
        divs = soup.find_all('div', {'lang': True})
        for div in divs:
            text = div.get_text(strip=True)
            if len(text) > 20:
                return text
        
        return None
    
    def _extract_general_text(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract text from general web pages."""
        # Try common content selectors
        selectors = [
            'main article',
            'article',
            '.content',
            '.post-content',
            '.entry-content',
            'main p',
            'body p'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                # Get all text from matching elements
                text = ' '.join([elem.get_text(strip=True) for elem in elements])
                if len(text) > 50:  # Only return if substantial
                    return text
        
        # Fallback: get title and meta description
        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        parts = []
        if title:
            parts.append(title.get_text(strip=True))
        if meta_desc and meta_desc.get('content'):
            parts.append(meta_desc.get('content'))
        
        return ' '.join(parts) if parts else None
    
    async def _add_cookies(self, context: BrowserContext, cookies_str: str, domain: str):
        """Parse and add cookies to browser context."""
        try:
            # Parse cookies from string format (key1=value1; key2=value2)
            cookies = []
            for cookie in cookies_str.split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    cookies.append({
                        'name': name,
                        'value': value,
                        'domain': domain,
                        'path': '/'
                    })
            
            await context.add_cookies(cookies)
        except Exception as e:
            print(f"Error adding cookies: {e}")

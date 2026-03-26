"""Twitter/X scraper using Playwright"""
import asyncio
from typing import List
from .base import BaseScraper, TravelContent
from playwright.async_api import async_playwright

class TwitterScraper(BaseScraper):
    """Scrape Twitter/X for travel content"""
    
    PLATFORM = "twitter"
    
    async def search(self, query: str, limit: int = 20) -> List[TravelContent]:
        """Search Twitter for travel tweets"""
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            # Twitter search
            search_url = f"https://twitter.com/search?q={query}%20travel&f=live"
            await page.goto(search_url)
            await page.wait_for_timeout(5000)
            
            # Extract tweets
            tweets = await page.query_selector_all('article[data-testid="tweet"]')
            
            for i, tweet in enumerate(tweets[:limit]):
                try:
                    text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                    text = await text_elem.inner_text() if text_elem else ""
                    
                    link_elem = await tweet.query_selector('a[href*="/status/"]')
                    url = await link_elem.get_attribute('href') if link_elem else ""
                    url = f"https://twitter.com{url}" if url else ""
                    
                    img_elem = await tweet.query_selector('img[src*="profile_images"]')
                    author = await img_elem.get_attribute('alt') if img_elem else "unknown"
                    
                    results.append(TravelContent(
                        platform=self.PLATFORM,
                        title=text[:100],
                        description=text,
                        location=self._extract_location(text),
                        hashtags=self._extract_hashtags(text),
                        image_url=None,
                        video_url=None,
                        url=url,
                        author=author,
                        likes=0,
                        created_at=None
                    ))
                except Exception as e:
                    print(f"Error extracting tweet {i}: {e}")
            
            await browser.close()
        
        return results
    
    async def get_trending(self, location: str, limit: int = 20) -> List[TravelContent]:
        """Get trending content"""
        return await self.search(f"{location}", limit)
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags"""
        import re
        return re.findall(r'#(\w+)', text)
    
    def _extract_location(self, text: str) -> str:
        """Extract location"""
        return ""

# Sync wrapper
def search_twitter(query: str, limit: int = 20) -> List[dict]:
    """Synchronous wrapper"""
    scraper = TwitterScraper()
    results = asyncio.run(scraper.search(query, limit))
    return [r.__dict__ for r in results]

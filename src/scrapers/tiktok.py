"""TikTok scraper using Playwright"""
import asyncio
from typing import List
from .base import BaseScraper, TravelContent
from playwright.async_api import async_playwright

class TikTokScraper(BaseScraper):
    """Scrape TikTok for travel content"""
    
    PLATFORM = "tiktok"
    
    async def search(self, query: str, limit: int = 20) -> List[TravelContent]:
        """Search TikTok for travel videos"""
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            # Search URL
            search_url = f"https://www.tiktok.com/search?q={query}%20travel"
            await page.goto(search_url)
            await page.wait_for_timeout(3000)
            
            # Extract video data
            videos = await page.query_selector_all('[data-e2e="search_video-item"]')
            
            for i, video in enumerate(videos[:limit]):
                try:
                    title = await video.get_attribute('aria-label') or ""
                    link = await video.query_selector('a')
                    url = await link.get_attribute('href') if link else ""
                    
                    results.append(TravelContent(
                        platform=self.PLATFORM,
                        title=title[:100],
                        description=title,
                        location=None,
                        hashtags=self._extract_hashtags(title),
                        image_url=None,
                        video_url=url,
                        url=url or f"https://tiktok.com/search?q={query}",
                        author="unknown",
                        likes=0,
                        created_at=None
                    ))
                except Exception as e:
                    print(f"Error extracting video {i}: {e}")
            
            await browser.close()
        
        return results
    
    async def get_trending(self, location: str, limit: int = 20) -> List[TravelContent]:
        """Get trending travel content for a location"""
        return await self.search(f"{location} travel", limit)
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        import re
        return re.findall(r'#(\w+)', text)

# Sync wrapper
def search_tiktok(query: str, limit: int = 20) -> List[dict]:
    """Synchronous wrapper for TikTok search"""
    scraper = TikTokScraper()
    results = asyncio.run(scraper.search(query, limit))
    return [r.__dict__ for r in results]

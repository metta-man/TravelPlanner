"""Instagram scraper using Playwright"""
import asyncio
from typing import List
from .base import BaseScraper, TravelContent
from playwright.async_api import async_playwright

class InstagramScraper(BaseScraper):
    """Scrape Instagram for travel content"""
    
    PLATFORM = "instagram"
    
    async def search(self, query: str, limit: int = 20) -> List[TravelContent]:
        """Search Instagram for travel posts"""
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            # Instagram探索页面
            search_url = f"https://www.instagram.com/explore/tags/{query.replace(' ', '')}travel/"
            await page.goto(search_url)
            await page.wait_for_timeout(3000)
            
            # 提取帖子
            posts = await page.query_selector_all('article a[href*="/p/"]')
            
            for i, post in enumerate(posts[:limit]):
                try:
                    url = await post.get_attribute('href')
                    url = f"https://www.instagram.com{url}" if url else ""
                    
                    img = await post.query_selector('img')
                    image_url = await img.get_attribute('src') if img else None
                    alt = await img.get_attribute('alt') if img else ""
                    
                    results.append(TravelContent(
                        platform=self.PLATFORM,
                        title=alt[:100] if alt else f"Instagram post {i+1}",
                        description=alt or "",
                        location=self._extract_location(alt),
                        hashtags=self._extract_hashtags(alt),
                        image_url=image_url,
                        video_url=None,
                        url=url,
                        author="unknown",
                        likes=0,
                        created_at=None
                    ))
                except Exception as e:
                    print(f"Error extracting post {i}: {e}")
            
            await browser.close()
        
        return results
    
    async def get_trending(self, location: str, limit: int = 20) -> List[TravelContent]:
        """Get trending content for a location"""
        return await self.search(location, limit)
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        import re
        return re.findall(r'#(\w+)', text)
    
    def _extract_location(self, text: str) -> str:
        """Extract location from text"""
        # Simple implementation - can be improved with NER
        if " in " in text.lower():
            parts = text.lower().split(" in ")
            if len(parts) > 1:
                return parts[1].split()[0].title()
        return ""

# Sync wrapper
def search_instagram(query: str, limit: int = 20) -> List[dict]:
    """Synchronous wrapper"""
    scraper = InstagramScraper()
    results = asyncio.run(scraper.search(query, limit))
    return [r.__dict__ for r in results]

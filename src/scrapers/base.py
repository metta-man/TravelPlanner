"""Base scraper class"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TravelContent:
    """Travel content from social media"""
    platform: str
    title: str
    description: str
    location: Optional[str]
    hashtags: List[str]
    image_url: Optional[str]
    video_url: Optional[str]
    url: str
    author: str
    likes: int
    created_at: datetime

class BaseScraper(ABC):
    """Base class for social media scrapers"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
    
    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[TravelContent]:
        """Search for travel content"""
        pass
    
    @abstractmethod
    async def get_trending(self, location: str, limit: int = 20) -> List[TravelContent]:
        """Get trending content for a location"""
        pass

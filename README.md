# 🗺️ TravelPlanner

Social media travel & weekend planner - Research destinations from Facebook, TikTok, X, Threads, Instagram.

## Features

- 🔍 **Multi-platform search** - Aggregate travel content from 5+ platforms
- 📍 **Destination research** - Find trending spots, hidden gems
- 📅 **Weekend planning** - Smart itinerary suggestions
- 💾 **Save & organize** - Bookmark favorite finds
- 🤖 **AI-powered** - Auto-summarize and extract key info

## Supported Platforms

| Platform | Status | Features |
|----------|--------|----------|
| **TikTok** | ✅ | Video search, trending hashtags |
| **Instagram** | ✅ | Location tags, reels, posts |
| **X (Twitter)** | ✅ | Travel threads, tips |
| **Facebook** | 🔄 | Groups, events |
| **Threads** | 🔄 | Travel discussions |

## Quick Start

```bash
# Clone
git clone https://github.com/metta-man/TravelPlanner.git
cd TravelPlanner

# Install
pip install -r requirements.txt

# Run
python src/main.py --destination "Tokyo" --platforms tiktok,instagram
```

## Tech Stack

- Python 3.11+
- Playwright (browser automation)
- OpenAI API (content analysis)
- Streamlit (web UI)

## Roadmap

- [ ] Basic multi-platform search
- [ ] AI content summarization
- [ ] Itinerary generator
- [ ] Price comparison integration
- [ ] Mobile app

## License

MIT

## Author

Created with ❤️ using OpenClaw

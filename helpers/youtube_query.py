from yt_dlp import YoutubeDL
from typing import List

def search_youtube_urls(query: str, max_results: int = 5) -> List[str]:
    """
    Searches YouTube for a query using yt-dlp and returns a list of video URLs.

    Args:
        query: The search query string (e.g., "best new songs").
        max_results: The maximum number of video URLs to return.

    Returns:
        A list of YouTube video URLs (watch links).
    """
    search_term = f"ytsearch{max_results}:{query}"

    ydl_opts = {
        'quiet': True,
        'flat_playlist': True,
        'extract_flat': True,
        'noplaylist': True,
        'skip_download': True, 
        'ignoreerrors': True,
    }

    video_urls = []
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=False)
            if info and 'entries' in info:
                for entry in info['entries']:
                    if entry and 'url' in entry:
                        video_urls.append(entry['url'])
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return video_urls

from typing import Optional 
import yt_dlp

def get_audio_stream_url(video_url: str) -> Optional[str]:
    """
    Uses yt-dlp to extract the direct audio stream URL from a video URL (e.g., YouTube).
    """
    ydl_opts = {
        'format': 'bestaudio', # No fallback to video, ensures audio-only
        'force_ipv4': True,    # Forces IPv4, can help avoid 429 errors on servers
        'noplaylist': True,
        'quiet': True,
        'default_search': 'auto', # Allows it to handle non-URL queries if needed
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False) 
            
            return info.get('url') 

    except yt_dlp.utils.DownloadError as e:
        print(f"yt-dlp DownloadError: {e}")
        return None
    except Exception as e:
        print(f"Error fetching audio stream: {e}")
        return None
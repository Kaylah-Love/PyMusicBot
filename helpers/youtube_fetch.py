# Make sure to install yt-dlp: pip install yt-dlp
import yt_dlp

def get_audio_stream_url(video_url: str) -> str | None:
    """
    Uses yt-dlp to extract the direct audio stream URL from a video URL (e.g., YouTube).
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info['url']
    except Exception as e:
        print(f"Error fetching audio stream: {e}")
        return None
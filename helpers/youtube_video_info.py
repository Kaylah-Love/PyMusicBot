import yt_dlp
import pprint # Used for pretty-printing the result

def get_video_info(url):
    """
    Extracts video information (title, length, uploader, etc.) from a given URL
    using yt-dlp without downloading the video.

    Args:
        url (str): The URL of the video.

    Returns:
        dict: A dictionary containing the video information, or None if an error occurs.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            summary = {
                'title': info_dict.get('title'),
                'uploader': info_dict.get('uploader'),
                'duration_seconds': info_dict.get('duration'),
                'view_count': info_dict.get('view_count'),
                'upload_date': info_dict.get('upload_date'),
                'webpage_url': info_dict.get('webpage_url'),
                'description': info_dict.get('description')
            }
            return summary

    except yt_dlp.utils.DownloadError as e:
        print(f"Error fetching video information for {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

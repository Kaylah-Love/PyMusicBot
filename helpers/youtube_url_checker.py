import re

def is_valid_youtube_url(url: str) -> bool:
    """
    Checks if a string is a valid YouTube video URL using a common regex pattern.
    """
    # This regex matches common YouTube watch URLs and shortened URLs.
    # It focuses on capturing the video ID for validation.
    youtube_regex = (
        r'(?:https?:\/\/)?'  # Optional http(s)://
        r'(?:www\.)?'        # Optional www.
        r'(?:'
        r'youtube\.com\/watch\?v=|' # youtube.com/watch?v=
        r'youtu\.be\/'              # youtu.be/
        r')'
        r'([a-zA-Z0-9_-]{11})' # The 11-character video ID group
    )
    
    # re.match attempts to match the pattern at the beginning of the string.
    # If a match is found, it returns a match object (which is truthy).
    if re.match(youtube_regex, url):
        return True
    return False
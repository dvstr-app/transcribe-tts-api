from pytube import YouTube
# from youtube_transcript_api import YouTubeTranscriptApi


def download_audio(video_url: str, out_path: str) -> str:
    """
    Downloads audio track of a youtube video given the url
    """
    path = YouTube(video_url).streams.filter(only_audio=True).first().download(out_path)
    return path


def extract_id(video_url: str) -> str:
    video = YouTube(video_url)
    return video.video_id


def get_embed_url(video_url):
    video_id = extract_id(video_url)
    return f"http://www.youtube.com/embed/{video_id}"


def get_title(video_url: str) -> str:
    video = YouTube(video_url)
    return video.title


# def get_captions_list(video_url: str) -> str:
#     video = YouTubeTranscriptApi()
#     return video.get_transcript(extract_id(video_url), languages=['en'])


import os
import tempfile
import youtube_dl


def download_video_and_audio(video_url: str) -> tuple:
    """Download video by url and store it by returned path."""
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'format': 'mp4',  # Video format
        'outtmpl': os.path.join(temp_dir, 'youtube.%(ext)s'),  # Output file name
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Audio format
            'preferredquality': '0'  # Audio quality
        }],
        'keepvideo': True  # Keep the video file after extracting audio
    }
    # Download the video and extract audio
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    video_file = os.path.join(temp_dir, 'youtube.mp4')
    audio_file = os.path.join(temp_dir, 'youtube.mp3')
    return video_file, audio_file


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=Fr_MHKIYBcg"
    video_path, audio_path = download_video_and_audio(url)
    print("Downloaded video has path:", video_path)
    print("Downloaded audio has path:", audio_path)

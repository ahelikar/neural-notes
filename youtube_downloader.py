import yt_dlp
import os

def download_youtube_audio(url):
    # Setup options to extract only audio and save as mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # This saves it as 'youtube_audio.mp3'
        'outtmpl': 'youtube_audio.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return "youtube_audio.mp3"
import yt_dlp
from time import sleep
from utils import SilentLogger


pandavideoheaders = lambda url: {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
  'Referer': f'{url}',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'no-cors',
  'Sec-Fetch-Site': 'cross-site',
  'Cache-Control': 'max-age=0',
  'Te': 'trailers'
}


def download_video(url, output_name, referer_url, max_retries=3, retry_delay=5):
  headers = pandavideoheaders(referer_url)
  ydl_opts = {
    'format': 'bv+ba/b',
    'outtmpl': output_name,
    'quiet': True,
    'no_progress': True,
    'http_headers': headers,
    'logger': SilentLogger(),
    'concurrent_fragment_downloads': 10,
    'fragment_retries': 50,
    'retry_sleep_functions': {'fragment': 30},
    'buffersize': 104857600,
    'retries': 20,
    'continuedl': True,
    'extractor_retries': 10,
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
import yt_dlp
from utils import SilentLogger, log_error


pandavideoheaders = lambda rerefer, optional_origin=None: {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Referer': rerefer,
  **({'Origin': optional_origin} if optional_origin is not None else {})
}


def verified_retry_download(url, session, ydl_opts):
  headers = pandavideoheaders(session.url, session.url)
  ydl_opts['http_headers'] = headers
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])


def download_video(url, output_name, session):
  headers = pandavideoheaders(session.url)
  ydl_opts = {
    'format': 'bv+ba/b',
    'outtmpl': output_name,
    'quiet': True,
    'no_progress': True,
    'http_headers': headers,
    'logger': SilentLogger(),
    'concurrent_fragment_downloads': 7,
    'fragment_retries': 50,
    'retry_sleep_functions': {'fragment': 30},
    'buffersize': 104857600,
    'retries': 30,
    'continuedl': True,
    'extractor_retries': 10,
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
  except yt_dlp.utils.DownloadError as e:
    if '403' in str(e) or '401' in str(e):
      verified_retry_download(url, session, ydl_opts)
    log_error(f"Erro ao baixar: {e}")
    pass
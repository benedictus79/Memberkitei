import yt_dlp
from time import sleep
from utils import SilentLogger, log_error


pandavideoheaders = lambda rerefer, optional_origin=None: {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Referer': rerefer,
  **({'Origin': optional_origin} if optional_origin is not None else {})
}

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
    'external_downloader': 'aria2c',
    'external_downloader_args': [
        '--allow-overwrite=true',
        '--file-allocation=none',
        '--console-log-level=error',
        '--download-result=hide',
        '--summary-interval=0',
        '-x16', '-j16', '-s16',
        '--max-connection-per-server=16',
        '--min-split-size=10M',
        '--split=16',
        '--optimize-concurrent-downloads',
        '--max-overall-download-limit=0',
        '--quiet=true'
          ]
                }
  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
  except yt_dlp.utils.DownloadError as e:
    if '403' in str(e) or '401' in str(e):
      verified_retry_download(url, session, ydl_opts)
    log_error(f"Erro ao baixar: {e}")
    pass


def verified_retry_download(url, session, ydl_opts):
  headers = pandavideoheaders(session.url, session.url)
  ydl_opts['http_headers'] = headers
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
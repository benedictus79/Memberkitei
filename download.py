import yt_dlp
from utils import SilentLogger, log_error


pandavideoheaders = lambda rerefer: {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Referer': rerefer,
}


def download_video(url, output_name, session=None):
  ydl_opts = {
    'format': 'bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best',
    'outtmpl': f'{output_name}.%(ext)s',
    'quiet': True,
    'no_progress': True,
    'logger': SilentLogger(url, f'{output_name}.%(ext)s'),
    'concurrent_fragment_downloads': 10,
    'fragment_retries': 50,
    'file_access_retries': 50,
    'retries': 50,
    'continuedl': True,
    'extractor_retries': 50,
    'trim_file_name': 249,
  }
  if session:
    headers = pandavideoheaders(session.url)
    ydl_opts['http_headers'] = headers
  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
  except yt_dlp.utils.DownloadError as e:
    log_error(f"Erro ao baixar: {e} ||| {url}")

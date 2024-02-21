from datetime import datetime
import os
import re


def benedictus_ascii_art():
  benedictus = """
     ___ ___ _  _ ___ ___ ___ ___ _____ _   _ ___ 
    | _ ) __| \| | __|   \_ _/ __|_   _| | | / __|
    | _ \ _|| .` | _|| |) | | (__  | | | |_| \__ \\
    |___/___|_|\_|___|___/___\___| |_|  \___/|___/
    
  Author: Benedictus ©
  Community: https://t.me/alex4ndriagroup
  Version: Beta 2.0
  """
  print(benedictus)


def clear_screen():
  os.system('cls || clear')


def create_folder(folder_name):
  path = os.path.join(os.getcwd(), folder_name)

  if not os.path.exists(path):
    os.mkdir(path)

  return path


def clear_folder_name(name):
  sanitized_name = re.sub(r'[<>:"/\\|?*]', ' ', name)
  sanitized_name = re.sub(r'\s+', ' ', sanitized_name).strip()

  return sanitized_name


def shorten_folder_name(full_path, max_length=210):
  if len(full_path) > max_length:
    num_chars_to_remove = len(full_path) - max_length
    directory, file_name = os.path.split(full_path)
    base_name, extension = os.path.splitext(file_name)
    num_chars_to_remove = min(num_chars_to_remove, len(base_name))
    shortened_name = base_name[:-num_chars_to_remove] + extension
    new_full_path = os.path.join(directory, shortened_name)
    return new_full_path
    
  return full_path


def format_url(video_url):
  pattern = r'https://player-vz-([a-zA-Z0-9-]+).tv.pandavideo.com.br/embed/\?v=([a-zA-Z0-9-]+)'
  match = re.search(pattern, video_url)
  if match:
    subdomain = match.group(1)
    extracted_part = match.group(2)
    video_url = f'https://b-vz-{subdomain}.tv.pandavideo.com.br/{extracted_part}/playlist.m3u8'
    return video_url


def save_html(soup, lesson_folder, lesson_title):
  content_materials = soup.find('div', class_='content__materials')

  if content_materials:
    content_materials.decompose()
  file_path = shorten_folder_name(os.path.join(lesson_folder, clear_folder_name(lesson_title + ".html")))

  if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as file:
      file.write(str(soup.prettify()))


def save_file(file_path, response):
  if not os.path.exists(file_path):
    with open(file_path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)


def generate_file_name(url, headers, default_name='downloaded_material'):
  extension_map = {
    'application/rar': '.rar',
    'application/zip': '.zip',
    'application/pdf': '.pdf',
    'text/html': '.html',
    'text/csv;charset=UTF-8': '.csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
  }

  content_type = headers.get('Content-Type', '').split(';')[0]
  extension = extension_map.get(content_type, '')
  content_disposition = headers.get('Content-Disposition', '')

  if 'filename=' in content_disposition:
    filename = re.findall('filename="?([^";]+)"?', content_disposition)
    if filename:
      return filename[0]
        
  url_file_name = os.path.basename(url).split('?')[0].split('#')[0]

  if url_file_name:
    return url_file_name
  
  return default_name + extension

def save_material(soup, lesson_folder, lesson_title):
  file_path = os.path.join(lesson_folder, lesson_title + ".html")

  if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as file:
      file.write(str(soup.prettify()))


def log_error(message):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open('errosdownload.txt', 'a') as file:
    file.write(f"{timestamp} - {message}\n")


def extract_subdomain(url):
  regex = r"https?://([^/]+)\.memberkit\.com\.br"
  match = re.search(regex, url)
  if match:
    subdomain = match.group(1)
    return subdomain


class SilentLogger(object):
  def debug(self, msg):
    pass

  def warning(self, msg):
    log_error(msg)
    pass

  def error(self, msg):
    log_error(msg)
    pass

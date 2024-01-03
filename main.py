from concurrent.futures import ThreadPoolExecutor
from login import vazandigitalsession, selected_course, BeautifulSoup
from utils import format_url, generate_file_name, log_error, os, clear_folder_name, create_folder, save_file, save_html, shorten_folder_name
from download import download_video
from tqdm import tqdm


def extract_section_details(section, index, main_course_folder):
  span_tag = section.find('span', class_='ml-2.5')

  if not span_tag:
    return None
  
  section_title_text = span_tag.text.strip()
  section_title = f'{index:03d} - {section_title_text}'
  section_folder =  create_folder(shorten_folder_name(os.path.join(main_course_folder, clear_folder_name(section_title))))

  return section_folder


def extract_lesson_details(section, section_folder):
  a_tag = section.find_all('a', class_='lesson__title')

  if not a_tag:
    return None
  
  lessons_details = {}

  for i, lesson in enumerate(a_tag, start=1):
    lesson_title_text = lesson.text.strip()
    lesson_title = f'{i:03d} - {lesson_title_text}' 
    lesson_folder = create_folder(shorten_folder_name(os.path.join(section_folder, clear_folder_name(lesson_title))))
    lesson_link = f'''https://vazan-conteudo-digital.memberkit.com.br{lesson['href']}'''
    lessons_details[lesson_title_text] = {'url': lesson_link, 'path': lesson_folder}

  return lessons_details


def lesson_material(soup, lesson_folder):
  target_a = soup.find_all('a', class_="attachment")
  
  if target_a:
    for i, target_div in enumerate(target_a, start=1):
      material_href = target_div.get('href')
      response = vazandigitalsession.get(f'https://vazan-conteudo-digital.memberkit.com.br{material_href}')
      if response.status_code != 200:
        msg_warning = f"Erro ao acessar {material_href}: Status Code {response.status_code}"
        log_error(msg_warning)
        return
      file_name = generate_file_name(response.url, response.headers)
      material_folder = create_folder(os.path.join(lesson_folder, 'material'))
      file_path = os.path.join(material_folder, f'{i:03d} - {clear_folder_name(file_name)}')
      save_file(file_path, response)

def lesson_text(soup, lesson_folder, lesson_title):
  target_div = soup.find('div', class_='mx-auto max-w-screen-xl px-4 pb-4 md:px-8 md:pb-8')

  if target_div:
    content = target_div.find('div', class_='lg:col-span-2')
    save_html(content, lesson_folder, lesson_title)


def find_and_download_video(lesson_link, lesson_folder, lesson_title):
  response_lesson = vazandigitalsession.get(lesson_link)
  soup = BeautifulSoup(response_lesson.text, 'html.parser')
  target_div = soup.find('div', class_="aspect-h-9 aspect-w-16 relative z-20")

  if target_div:
    video_url = target_div.get('data-panda-player-url-value')
    if video_url:
      video_url = format_url(video_url)
      output_path = shorten_folder_name(os.path.join(lesson_folder, f'{clear_folder_name(lesson_title)}.mp4'))
      download_video(video_url, output_path, response_lesson)

  lesson_material(soup, lesson_folder)
  lesson_text(soup, lesson_folder, lesson_title)
  
      

def process_lessons(lessons):
  if lessons:
    for lesson, lesson_info in lessons.items():
      find_and_download_video(lesson_info['url'], lesson_info['path'], lesson)


def list_sections(course_name, course_link):
  main_course_folder = create_folder(clear_folder_name(course_name))
  response = vazandigitalsession.get(course_link)
  soup = BeautifulSoup(response.text, 'html.parser')
  sections = soup.find_all('div', class_='section')

  with ThreadPoolExecutor(max_workers=3) as executor:
    main_progress_bar = tqdm(total=len(sections), desc=course_name, leave=True)
    futures = []

    for i, section in enumerate(sections, start=1):
      section_folder = extract_section_details(section, i, main_course_folder)
      if section_folder:
        lessons = extract_lesson_details(section, section_folder)
        future = executor.submit(process_lessons, lessons)
        futures.append(future)

    for future in futures:
      future.result()
      main_progress_bar.update(1)

    main_progress_bar.close()


if __name__ == '__main__':
  course_name, course_link = selected_course
  list_sections(course_name, course_link)

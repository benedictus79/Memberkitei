import requests
from bs4 import BeautifulSoup
from utils import re, benedictus_ascii_art, clear_screen, extract_subdomain


vazandigitalsession = requests.Session()


headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'accept-language': 'pt-BR,pt;q=0.7',
  'cache-control': 'no-cache',
  'dnt': '1',
  'pragma': 'no-cache',
  'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'sec-gpc': '1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_authenticity_token():
  subdomain = input('Digite a url da pagina: ')
  subdomain = extract_subdomain(subdomain)
  headers['authority'] = f'https://{subdomain}.memberkit.com.br/'
  response = vazandigitalsession.get(f'https://{subdomain}.memberkit.com.br/users/sign_in', headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  token_element = soup.find('input', {'name': 'authenticity_token'})
  if token_element:
    authenticity_token = token_element['value']
    return authenticity_token, subdomain
  

def login(authenticity_token, subdomain):
  benedictus_ascii_art()
  username = input('email: ')
  password = input('senha: ')
  clear_screen()
  data = {
    'user[email]': username,
    'user[password]': password,
    'authenticity_token': authenticity_token,
    'user[remember_me]': 'true',
    'commit': 'Login',
  }
  response = vazandigitalsession.post(
    f'https://{subdomain}.memberkit.com.br/users/sign_in',
    headers=headers,
    data=data,
  )
  soup = BeautifulSoup(response.text, 'html.parser')
  href_pattern = re.compile(r"/\d+-[\w-]+")
  a_tag = soup.find_all('a', class_=['text-base font-medium tracking-tight text-inherit', 'block'])

  courses = {}
  for tag in a_tag:
    href = tag.get('href')
    if href and href_pattern.match(href):
        courses[tag.text.strip()] = f'https://{subdomain}.memberkit.com.br{href}'
    elif a_tag:
      courses[tag.text] = f'''https://{subdomain}.memberkit.com.br/{tag.get('href')}'''
  return courses


def choose_course(courses):
  print("Cursos disponíveis:")
  for i, course_title in enumerate(courses.keys(), start=1):
    print(f"{i}. {course_title}")

  choice = input("Escolha um curso pelo número: ")
  selected_course_title = list(courses.keys())[int(choice) - 1]
  selected_course_link = courses[selected_course_title]

  return selected_course_title, selected_course_link
  

token, subdomain = get_authenticity_token()
courses = login(token, subdomain)
selected_course = choose_course(courses)

import requests
from bs4 import BeautifulSoup
from utils import benedictus_ascii_art, clear_screen


vazandigitalsession = requests.Session()


headers = {
  'authority': 'vazan-conteudo-digital.memberkit.com.br',
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
  response = vazandigitalsession.get('https://vazan-conteudo-digital.memberkit.com.br/users/sign_in', headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  token_element = soup.find('input', {'name': 'authenticity_token'})
  if token_element:
    authenticity_token = token_element['value']
    return authenticity_token
  

def login(authenticity_token):
  benedictus_ascii_art()
  username = input("email: ")
  password = input("senha: ")
  clear_screen()
  data = {
    'user[email]': username,
    'user[password]': password,
    'authenticity_token': authenticity_token,
    'user[remember_me]': 'true',
    'commit': 'Login',
  }
  response = vazandigitalsession.post(
    'https://vazan-conteudo-digital.memberkit.com.br/users/sign_in',
    headers=headers,
    data=data,
  )
  soup = BeautifulSoup(response.text, 'html.parser')
  a_tag = soup.find_all('a', class_='text-base font-medium tracking-tight text-inherit')

  courses = {}
  if a_tag:
    for course in a_tag:
      courses[course.text] = f'''https://vazan-conteudo-digital.memberkit.com.br/{course.get('href')}'''

    return courses


def choose_course(courses):
  print("Cursos disponíveis:")
  for i, course_title in enumerate(courses.keys(), start=1):
    print(f"{i}. {course_title}")

  choice = input("Escolha um curso pelo número: ")
  selected_course_title = list(courses.keys())[int(choice) - 1]
  selected_course_link = courses[selected_course_title]

  return selected_course_title, selected_course_link
  

token = get_authenticity_token()
courses = login(token)
selected_course = choose_course(courses)



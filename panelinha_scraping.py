import requests
from bs4 import BeautifulSoup

base_url = 'https://panelinha.com.br/categoria/doces'

def get_html(url):
    response = requests.get(url)
    if response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding
    html = response.text
    return BeautifulSoup(html, 'html.parser')

def get_number_of_pages():
    main_page = get_html(base_url)
    pagination_links = main_page.find_all('a', class_='ais-Pagination-link')
    last_page_link = pagination_links.pop().get('href')
    number_of_pages = int(last_page_link.split('/').pop())
    return number_of_pages

def get_all_recipes():
    recipe_list = []
    for i in range(get_number_of_pages()):
        url = base_url+f'/pagina/{i+1}'
        html_page = get_html(url)
        recipes = html_page.find_all('div', class_='f fc mod')
        for recipe in recipes:
            recipe_list.append({
                'name': str(recipe.find('h6').text.strip()),
                'link': recipe.find('a').get('href'),
                'img': recipe.find('img').get('src')
            })
    return recipe_list

#Prox passos: explorar o link de cada receita e extrair ingredientes, preparo ...
recipes = get_all_recipes()
for recipe in recipes:
    print(recipe['name'])
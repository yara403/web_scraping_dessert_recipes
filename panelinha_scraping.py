import requests
from bs4 import BeautifulSoup

base_url = 'https://panelinha.com.br/categoria/doces'

def get_html(url):
    response = requests.get(url)
    if response.encoding == 'ISO-8859-1':
        response.encoding = 'UTF-8'#response.apparent_encoding
    html = response.text
    return BeautifulSoup(html, 'html.parser')

def get_number_of_pages():
    main_page = get_html(base_url)
    pagination_links = main_page.find_all('a', class_='ais-Pagination-link')
    last_page_link = pagination_links.pop().get('href')
    number_of_pages = int(last_page_link.split('/').pop())
    return number_of_pages

def get_all_recipes() -> list:
    recipe_list = []
    for i in range(get_number_of_pages()):
        url = base_url+f'/pagina/{i+1}'
        html_page = get_html(url)
        recipes = html_page.find_all('div', class_='f fc mod')
        for recipe in recipes:
            link = requests.compat.urljoin(base_url, recipe.find('a').get('href'))
            full_recipe = {
                'name': str(recipe.find('h6').text.strip()),
                'category': 'doces',
                'link': link,
                'img': recipe.find('img').get('src')
            }
            recipe_page = get_html(link)
            full_recipe['description'] = get_description(recipe_page)
            full_recipe['ingredients'] = get_ingredients(recipe_page)
            full_recipe['author'] = ''
            full_recipe['steps'] = []
            full_recipe['time'] = ''
            full_recipe['serves'] = ''
            full_recipe['nutrients'] = {}
            recipe_list.append(full_recipe)
    return recipe_list

def get_description(recipe) -> str:
    recipe_description = recipe.find('div', id='recipe_header')
    return recipe_description.find('p').text.strip()

def get_ingredients(recipe) -> list:
    sub_headers = recipe.findAll('h5')
    ingredient_sections = [h5 for h5 in sub_headers if h5.text.lower() == 'ingredientes']
    ingredients = []
    for section in ingredient_sections:
        ingredients_ul = section.find_next_sibling()
        ingredients.append([li.text.strip() for li in ingredients_ul.children if li.text.strip() != ''])
        
    return ingredients

all_recipes = get_all_recipes()
print(all_recipes[:10])
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random

with open('posts_urls3.csv', 'a', encoding='utf-8') as file:
    file.close()

with open('posts_urls3.csv', 'r', encoding='utf-8') as file:
    src = file.read()
    file.close()

with open('finish_pages3.csv', 'a', encoding='utf-8') as file:
    file.close()

with open('posts_urls3.csv', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    file.close()

with open('finish_pages3.csv', 'r', encoding='utf-8') as file:
    finished_urls = file.read().split('\n')
    file.close()


def post_url_writer(link: str) -> None:
    with open('posts_urls3.csv', 'a', encoding='utf-8') as file:
        if not link in src:
            file.write(str(link) + '\n')
            file.close()


def finish_writer(link: str) -> None:
    with open('finish_pages3.csv', 'a', encoding='utf-8') as file:
            file.write(str(link) + '\n')
            file.close()


def error_writer(link: str, e: str) -> None:
    with open('error_pages3.csv', 'a', encoding='utf-8') as file:
            file.write(f'{str(link)}, {e} + "\n"')
            file.close()


def post_text_writer(text: str, file_name: str) -> None:
    with open(f'articles3/{file_name}.txt', 'w', encoding='utf-8') as file:
        file.write(text + '\n')
        file.close()

def parser(url: str) -> None:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    for post in soup.find_all('a', class_='media-list__head'):
        post_url = post.get('href')
        print('Ссылка на пост: ', post_url)
        post_url_writer(post_url)


def post_text_get(product_link: str) -> None:
    if not product_link in finished_urls:
        try:
            r = requests.get(product_link)
            soup = BeautifulSoup(r.content, features='html.parser')
            title = soup.find('h1', class_='page-main__head').text
            article_text = soup.find('div', class_='page-main__text').find_all('p')
            text = ''
            for paragraph in article_text:
                text += paragraph.text.replace(' ', '').strip() + '\n'
            full_article_text = title + '\n' + text
            file_name = f'{random.randint(1, 10000)}{random.randint(1, 10000)}{random.randint(1, 10000)}'
            if 'ә' in full_article_text or 'ү' in full_article_text or 'һ' in full_article_text or 'ө' in full_article_text or 'җ' in full_article_text or 'ң' in full_article_text:
                post_text_writer(full_article_text, file_name)
                print(file_name, 'записан')
                finish_writer(product_link)
            else:
                print('Нет татарских букв:', product_link)
        except Exception as e:
            print(e)
            error_writer(product_link, str(e))
    else:
        print('Уже записана ', product_link)


def main() -> None:
    for i in range(1, 2000):
        url = f'http://shahrikazan.ru/news/widget/list/poslednie-novosti/page/{i}'
        print('Пробуем: ', file)
        try:
            parser(url)
        except Exception as e:
            print(e)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(post_text_get, data)
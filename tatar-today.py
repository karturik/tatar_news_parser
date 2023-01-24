import requests
from bs4 import BeautifulSoup
import threading
import random
import concurrent.futures

# GET DATA FROM SAVED FILES
with open('posts_urls.csv', 'r', encoding='utf-8') as file:
    src = file.read()
    file.close()

with open('posts_urls.csv', 'r', encoding='utf-8') as file:
    data = file.read().split('\n')
    file.close()

with open('finish_pages.csv', 'r', encoding='utf-8') as file:
    finished_urls = file.read().split('\n')
    file.close()


def post_url_writer(link: str) -> None:
    with open('posts_urls.csv', 'a', encoding='utf-8') as file:
        if not link in src:
            file.write(str(link) + '\n')
            file.close()


def finish_writer(link: str) -> None:
    with open('finish_pages.csv', 'a', encoding='utf-8') as file:
            file.write(str(link) + '\n')
            file.close()


def error_writer(link: str, e: str) -> None:
    with open('error_pages.csv', 'a', encoding='utf-8') as file:
            file.write(f'{str(link)}, {e} + "\n"')
            file.close()


def post_text_writer(text: str, file_name: str) -> None:
    with open(f'articles/{file_name}.txt', 'w', encoding='utf-8') as file:
        file.write(text + '\n')
        file.close()


def parser(url: str) -> None:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    for post in soup.find_all('li', class_='list-post pclist-layout'):
        if not 'Татар ашлары' in post.text:
            post_url = post.find('a', class_='penci-btn-readmore').get('href')
            print(post_url)
            post_url_writer(post_url)


def post_text_get(product_link: str) -> None:
    if not product_link in finished_urls:
        try:
            r = requests.get(product_link)
            soup = BeautifulSoup(r.content, features='html.parser')
            title = soup.find('h1', class_='post-title single-post-title entry-title').text
            article_text = soup.find('div', class_='inner-post-entry entry-content').find_all('p')
            text = ''
            for paragraph in article_text:
                text += paragraph.text.replace(' ', '').strip() + '\n'
            full_article_text = title + '\n' + text
            file_name = product_link.split('/')[-2]
            post_text_writer(full_article_text, file_name)
            print(file_name, 'записан')
            finish_writer(product_link)
        except Exception as e:
            print(e)
            error_writer(product_link, str(e))
    else:
        print('Уже записана ', product_link)


def main() -> None:
    for i in range(1, 885):
        url = f'https://tatar-today.ru/category/news/tatarstan/page/{i}/'
        try:
            parser(url)
        except Exception as e:
            print(e)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(post_text_get, data)


if __name__ == '__main__':
    main()
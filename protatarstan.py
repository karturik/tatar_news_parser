import requests
from bs4 import BeautifulSoup
import concurrent.futures

# GET DATA FROM SAVED FILES
with open('posts_urls1.csv', 'ar', encoding='utf-8') as file:
    data = file.read().split('\n')
    file.close()

with open('finish_pages1.csv', 'ar', encoding='utf-8') as file:
    finished_urls = file.read().split('\n')
    file.close()

with open('posts_urls1.csv', 'r', encoding='utf-8') as file:
    src = file.read()
    file.close()


def post_url_writer(link: str) -> None:
    with open('posts_urls1.csv', 'a', encoding='utf-8') as file:
        if not link in src:
            file.write(str(link) + '\n')
            file.close()


def post_text_writer(text: str, file_name: str) -> None:
    with open(f'articles1/{file_name}.txt', 'w', encoding='utf-8') as file:
        file.write(text + '\n')
        file.close()


def finish_writer(link: str) -> None:
    with open('finish_pages1.csv', 'a', encoding='utf-8') as file:
            file.write(str(link) + '\n')
            file.close()


def error_writer(link: str, e: str) -> None:
    with open('error_pages1.csv', 'a', encoding='utf-8') as file:
            file.write(f'{str(link)}, {e} + "\n"')
            file.close()


def parser(url: str) -> None:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='html.parser')
    for post in soup.find_all('div', class_='desc'):
        post_url = post.find_all('a')[1].get('href')
        print('Ссылка на пост: ', post_url)
        post_url_writer(post_url)


def post_text_get(product_link: str) -> None:
    if not product_link in finished_urls:
        try:
            r = requests.get(product_link)
            soup = BeautifulSoup(r.content, features='html.parser')
            title = soup.find('h1').text
            article_text = soup.find('div', class_='post').find_all('p')
            text = ''
            for paragraph in article_text:
                text += paragraph.text.replace(' ', '').strip() + '\n'
            full_article_text = title + '\n' + text
            file_name = product_link.split('/')[-2]
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
    for i in range(1, 8):
        url = f'http://protatarstan.ru/category/razumnoe-tat/page/{i}/'
        print('Пробуем: ', url)
        try:
            parser(url)
        except Exception as e:
            print(e)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(post_text_get, data)


if __name__ == '__main__':
    main()
import re
import requests
from bs4 import BeautifulSoup


def add_to_file(filename, lines):
    '''Фугкция добавляет статьи в файл'''
    with open(filename, 'a', encoding='utf-8') as file:
        file.writelines(lines)


def get_text(ref, filename):
    '''Функция берет необходимую информацию с сайта и отправляет в файл'''
    source = 'Благодарненские вести\n'  # источник
    url = ref  # ссылка на страницу с новостными статьями
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    for a in soup.find_all("a"):
        try:
            if "round-div" in a['class']:
                new_url = a['href']  # ссылка на статью
                new_response = requests.get(new_url)
                new_soup = BeautifulSoup(new_response.text, features="html.parser")
                text = new_soup.get_text() + '\n'
                naked_text = re.sub('  Skip to .+[0-3]\d\.[01]\d.20[0-2]\d', '', text)  # текст статьи
                date = re.findall(r'[0123]\d\.[01]\d\.20[012]\d', text)[0] + '\n'  # дата
                new_url = new_url + '\n'  # ссылка на статью для файла
                author = '-\n'  # автор (которого нет)
                lines = ['=====\n', new_url, source, date, author,  naked_text]  # вся необходимая информация\
                # в одном списке
                add_to_file(filename, lines)  # добавляем все это в файл
        except:
            pass
        try:
            if 'meta-nav' in a.contents[0]['class']:
                # print(a)
                # переходим на следующую страницу
                new_url = a['href']
                get_text(new_url, filename)
        except:
            pass


def main():
    ref = "http://blag-vesti.ru/"  # ссылка на сайт, который надо обкачать
    get_text(ref, 'news_texts3.txt')


if __name__ == '__main__':
    main()


import os
from datetime import datetime
import requests
import bs4

def logger(old_function):
    def new_function(*args, **kwargs):
        func_time = datetime.now()
        old_func_name = old_function.__name__
        res = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'Дата и время вызова функции - {func_time}, \n'
                       f'имя функции - {old_func_name}, '
                       f'аргументы функции - {args, kwargs}, '
                       f'значение функции - {res}')
        return res
    return new_function


def logger_func(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            func_time = datetime.now()
            old_func_name = old_function.__name__
            res = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'Дата и время вызова функции - {func_time}, \n'
                           f'имя функции - {old_func_name}, '
                           f'аргументы функции - {args, kwargs}, '
                           f'значение функции - {res}')
            return res
        return new_function
    return __logger


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(a=2, b=2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(a=6, b=2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(a=4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_func(path)
        def hello_world():
            return 'Hello World'

        @logger_func(path)
        def summator(a, b=0):
            return a + b

        @logger_func(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__=='__main__':
    test_1()
    test_2()

#Применение к прошлой ДЗ
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/all/'
response = requests.get(url)
soup=bs4.BeautifulSoup(response.text, features='lxml')

articles = soup.findAll('article', class_='tm-articles-list__item')

previews = dict()
for article in articles:
    date = article.time.text
    preview = article.find('h2', class_='tm-title tm-title_h2')
    title= article.find('a', class_='tm-title__link')
    href = title['href']
    previews.setdefault(date, [preview.text.strip(), url+href])
    print(f'<{date}>-<{preview.text.strip()}>-<{url +href}>')
@logger
def result(KEYWORDS):
    for i in KEYWORDS:
        for j, k in previews.items():
            if i in k[0]:
                print(f'\n Результат поиска: "{i}": <{j}>-<{k[0]}>-><{k[1]}>')
                return k[0]
result(KEYWORDS)
            
import requests
from bs4 import BeautifulSoup
import string
import os

n_pages = int(input('Input the number of pages to parse: '))
article_type = input('Input the article type: ')

current = os.getcwd()

for i in range(1, n_pages + 1):
    os.mkdir(f'{current}\Page_{i}')
    os.chdir(f'{current}\Page_{i}')
    r = requests.get('https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=' + str(i))

    data = BeautifulSoup(r.content, 'html.parser' )

    article = data.find_all('article')

    new_articles = []
    for a in article:
        if article_type == a.find('span', {'class': "c-meta__type"}).text:
            name = a.find('a',{'data-track-label':"link"}).text
            translator = name.maketrans('', '', string.punctuation)
            translated_name = name.translate(translator).replace(' ', '_')
            newa_articles.append(translated_name)
            cont = requests.get('https://www.nature.com' + a.find('a').get('href'))
            article_html = BeautifulSoup(cont.content, 'html.parser')
            body = article_html.find('div', {'class': 'article__body cleared'})
            file = open(translated_name + '.txt', 'w', encoding="utf-8")
            if body:
                paragrafs = body.find_all('p')
                lst = [i.text for i in paragrafs]
                file.write(name.strip() + '\n')
                file.write('\n'.join(lst).strip())
                file.close()
    os.chdir(current)

print('Success')

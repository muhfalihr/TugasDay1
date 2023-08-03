import hashlib
from langdetect import detect
from bs4 import BeautifulSoup
import requests
import datetime
import re
import json


user_agent = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'}

link = "https://www.kompas.com/global/read/2023/08/02/095400370/wali-kota-di-meksiko-dikecam-karena-hadirkan-penari-striptis-dalam?page=all"

req = requests.get(link, headers=user_agent)

datas = BeautifulSoup(req.text, 'html.parser')

items, __content, __hashtags = datas.find_all(
    'div', 'content_article'), datas.find_all('div', 'read__content'), datas.find_all('ul', 'mob-tagging__items')


def cleanUniqcode(text):
    pattern = r'[^\x00-\x7F]+'
    return re.sub(pattern, 'a', text)


listLink = link.split('/')

for item in items:
    hypeTag = ''.join(
        item.find('div', 'exp-tag-populer').div.text.split('\n'))
    image = item.find(
        'div', 'imgHL').div.img['src']
    source = item.find('div', 'read__date').a.text
    __hour = int(listLink[8][:2])
    __minute = int(listLink[8][2:4])
    __second = int(listLink[8][4:6])
    __year = int(listLink[5])
    __mounth = int(listLink[6][1])
    __date = int(listLink[7])
    pub_hour = ''.join(
        str(datetime.date(__year, __mounth, __date)).split('-'))
    pub_minute = f'{pub_hour}' + \
        ''.join(str(datetime.time(__hour, __minute)).split(':')[:-1])
    pub_year = __year
    pub_day = str(datetime.datetime(__year, __mounth, __date).strftime('%A').replace('Sunday', 'Minggu').replace('Monday', 'Senin').replace(
        'Tuesday', 'Selasa').replace('Wednesday', 'Rabu').replace('Thursday', 'Kamis').replace('Friday', 'Jumat').replace('Saturday', 'Sabtu'))
    created_at = str(datetime.datetime(
        __year, __mounth, __date, __hour, __minute, __second))
    title = item.find('h1', 'read__title').text
    editor = item.find('div', 'read__credit').h6.a.text
    author = item.find('div', 'read__credit__logo').a.text
    time_zone = str(datetime.datetime(__year, __mounth, __date,
                    __hour, __minute, __second).astimezone())[-6:]
htag = []
for hashtag in __hashtags:
    hashtaggg = hashtag.find_all('a')
    for h in hashtaggg:
        htag.append('#' + h.text)
hashtags = ','.join(htag)
konten = []
for cont in __content:
    _cont = cont.find_all('p')
    for c in _cont:
        konten.append(''.join(c.find_all(string=True, recursive=False)))
content_cleaned = [cleanUniqcode(paragraph) for paragraph in konten]
content = ''.join(content_cleaned)
id = str(hashlib.md5(link.encode()).hexdigest())
lang = str(detect(datas.get_text()))
crawlingDate = str(datetime.datetime.now())
desc = '{0}{1}'.format(content[:100], '...')

datas = []
datas.append({
    "hashtags": hashtags,
    "pub_hour": pub_hour,
    "link": link,
    "created_at": created_at,
    "source": source,
    "title": title,
    "content": content,
    "pub_minute": pub_minute,
    "pub_year": pub_year,
    "id": id,
    "lang": lang,
    "editor": editor,
    "author": author,
    "pub_day": pub_day,
    "time_zone": time_zone,
    "crawlingDate": crawlingDate,
    "desc": desc
})

jsons = json.dumps(datas)

try:
    with open('data.json', 'w') as file:
        file.write(jsons)
except:
    with open('data.json', 'r+') as file:
        file.write(jsons)

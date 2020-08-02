from bs4 import BeautifulSoup
from datetime import datetime
from io_tools import outCsv

import requests
import json
import re
import time

URL = 'http://anitsayac.com/'

def main():
    date = datetime.strftime(datetime.now(), '%Y%m%d')
    cache_dict = get_cache('anitsayac_cache.json')

    res = requests.get(URL)
    soup = BeautifulSoup(res.content, features='lxml')
    feminisits = []
    for feminisit in soup.findAll('span', {'class':'xxy'}):
        a = feminisit.findChild('a')
        isim = a.getText()
        link = a.get('href')
        feminisits.append({'isim':isim, 'link':URL+link})
    with open('ref.json', 'w') as out:
        json.dump(feminisits, out, indent=2)

    feminisit_veri = []
    count = 0
    for f in feminisits:
        if f['link'] in cache_dict:
            veri = cache_dict[f['link']]
        else:
            print(f['isim'], 'not in cache')
            veri = get_data(f['link'])
            time.sleep(0.5)
        if veri:
            veri.update(f)
            feminisit_veri.append(veri)
            count += 1
            if count%50 == 0:
                print(count,'/',len(feminisits))
                with open('anitsayac_cache.json', 'w') as out:
                    json.dump(feminisit_veri, out, indent=2)

    with open('anitsayac_%s.json'%date, 'w') as out:
        json.dump(feminisit_veri, out, indent=2)

    keys = feminisit_veri[0].keys()
    outCsv(keys, feminisit_veri, 'anitsayac_%s.csv'%date) 

def get_cache(filename):
    cache = json.load(open(filename))
    cache_dict = {}
    for c in cache:
        cache_dict[c['link']] = c
    return cache_dict

def get_data(url):
    res = requests.get(url)
    try:
        soup = BeautifulSoup(res.content, features='lxml')
    except Exception as e:
        print(url)
        print(e)
        return {}
    return parse_data(soup)

def parse_data(soup):
    body = soup.find('body')
    body_html = str(body)
    keys = [b.getText() for b in body.findAll('b')]
    q = '(\<b\>%s\<\/b\>)(.+?)\<'
    data = {}
    for key in keys:
        m = re.search(q%key, body_html)
        if not m:
            print(body_html)
            return {}
        data[key.strip()] = m.groups()[1].strip()
    # simdilik sadece tek kaynak URL aliyor
    if body.find('a'):
        data['Kaynak:'] = body.find('a').get('href')
    if body.find('img'):
        data['Gorsel:'] = body.find('img').get('src')
    return data

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os, urllib.request, urllib.parse, json, sys

os.makedirs('images', exist_ok=True)

mapping = {
    'index-hero': 'chinese restaurant dish',
    'menu-hero': 'chinese dishes table',
    'about-hero': 'kitchen wok chef',
    'contact-hero': 'restaurant exterior storefront',
    'spring-rolls': 'spring rolls',
    'potstickers': 'potstickers',
    'crab-rangoon': 'crab rangoon',
    'sweet-and-sour': 'sweet and sour pork',
    'beef-broccoli': 'beef broccoli',
    'mapo-tofu': 'mapo tofu',
    'general-tso': "general tso's chicken",
    'lo-mein': 'lo mein noodles',
    'chow-mein': 'chow mein noodles',
    'fried-rice': 'fried rice'
}

API = 'https://commons.wikimedia.org/w/api.php'
HEADERS = {'User-Agent': 'local-biz-agent/1.0'}


def api_get(params):
    qs = urllib.parse.urlencode(params)
    url = API + '?' + qs
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)

for fname, term in mapping.items():
    try:
        print('Searching for:', term)
        params = {'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': term, 'srnamespace': 6, 'srlimit': 1}
        j = api_get(params)
        searches = j.get('query', {}).get('search', [])
        if not searches:
            print('  No file search result for', term)
            continue
        title = searches[0].get('title')
        print('  Found file title:', title)
        params = {'action': 'query', 'format': 'json', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url'}
        j2 = api_get(params)
        pages = j2.get('query', {}).get('pages', {})
        if not pages:
            print('  No pages for', title)
            continue
        page = list(pages.values())[0]
        imginfo = page.get('imageinfo')
        if not imginfo:
            print('  No imageinfo for', title)
            continue
        img_url = imginfo[0].get('url')
        if not img_url:
            print('  No url for', title)
            continue
        ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1]
        save_path = os.path.join('images', fname + ext)
        print('  Downloading', img_url)
        urllib.request.urlretrieve(img_url, save_path)
        print('  Saved to', save_path)
    except Exception as e:
        print('  Error for', term, e)

print('Done')

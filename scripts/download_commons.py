#!/usr/bin/env python3
import os, re, urllib.request, urllib.parse, json

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
headers = {'User-Agent': 'local-biz-agent/1.0'}

def fetch_text(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='ignore')

for fname, term in mapping.items():
    print('Searching for:', term)
    q = urllib.parse.quote(term)
    search_url = f'https://commons.wikimedia.org/w/index.php?title=Special:MediaSearch&search={q}&type=image'
    try:
        html = fetch_text(search_url)
    except Exception as e:
        print('Search failed for', term, e)
        continue
    m = re.search(r'/wiki/File:[^"\']+', html)
    if not m:
        print('No File found for', term)
        continue
    file_path = m.group(0)
    file_title = urllib.parse.unquote(file_path.split('/wiki/')[1])
    print('Found file page:', file_title)
    api = 'https://commons.wikimedia.org/w/api.php'
    params = urllib.parse.urlencode({
        'action':'query','format':'json','titles':file_title,'prop':'imageinfo','iiprop':'url'
    })
    try:
        with urllib.request.urlopen(api + '?' + params, timeout=15) as resp:
            j = json.load(resp)
    except Exception as e:
        print('API error for', file_title, e)
        continue
    pages = j.get('query', {}).get('pages', {})
    if not pages:
        print('No API page for', file_title)
        continue
    page = list(pages.values())[0]
    imginfo = page.get('imageinfo')
    if not imginfo:
        print('No imageinfo for', file_title)
        continue
    img_url = imginfo[0].get('url')
    if not img_url:
        print('No direct image URL for', file_title)
        continue
    ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1]
    save_path = os.path.join('images', fname + ext)
    print('Downloading', img_url)
    try:
        urllib.request.urlretrieve(img_url, save_path)
        print('Saved to', save_path)
    except Exception as e:
        print('Download failed for', img_url, e)
print('Done')

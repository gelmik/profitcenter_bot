import requests
import re

s = "funcjs['open_window_ads_in']('http://oceanwm.ru/video_good.php?site=profitcentr.com&id=854209&id_status=849670764&id_video=Fl88ngjN5tQ&timer=15&hash=763e76ec4b1853a4fafa7d747c4ebfe8');"

_hash = re.search(r"hash=(?P<hash>\w{32})", s).group('hash')
_id = re.search(r"id=(?P<_id>\d+)", s).group('_id')
_ids = re.search(r"id_status=(?P<_ids>\d+)", s).group('_ids')
video = re.search(r"id_video=(?P<video>.+)&timer", s).group('video')

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://oceanwm.ru',
    'pragma': 'no-cache',
    'referer': 'https://oceanwm.ru/',
    'sec-ch-ua': '"Opera GX";v="109", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0 (Edition Yx GX)',
}

data = {
    'func': 'ads-status',
    'code': '1',
    'hash': _hash,
    'ids': _ids,
    'id': _id,
    'video': video,
}

response = requests.post('https://profitcentr.com/ajax/earnings/ajax-youtube-in.php', headers=headers, data=data)
a = 1
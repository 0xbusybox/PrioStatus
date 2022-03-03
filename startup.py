import browser_cookie3 as bc3
import requests
import re
import random

STATUS_URL = 'https://raw.githubusercontent.com/0xbusybox/PrioStatus/main/status_texts/qoutes.txt'
REQUIRED_COOKIES = ['c_user', 'datr', 'fr', 'sb', 'xs']
PROXY = False

def hash_all_cookies(cookies):
    for i in REQUIRED_COOKIES:
        try:
            t = cookies[i]
        except:
            return False
    return True

def get_cookies():
    try:
        cookies = bc3.firefox(domain_name='facebook.com')
        cookies = requests.utils.dict_from_cookiejar(cookies)
        if(hash_all_cookies(cookies)):
            return cookies
    except:
        pass
    try:
        cookies = bc3.chrome(domain_name='facebook.com')
        cookies = requests.utils.dict_from_cookiejar(cookies)
        if(hash_all_cookies(cookies)):
            return cookies
    except:
        pass
    try:
        cookies = bc3.edge(domain_name='facebook.com')
        cookies = requests.utils.dict_from_cookiejar(cookies)
        if(hash_all_cookies(cookies)):
            return cookies
    except:
        pass

def post_status(status, cookies):
    try:
        session = requests.Session()
        session.cookies = requests.utils.cookiejar_from_dict(cookies)
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
        if PROXY:
            session.verify = False
            session.proxies = {'https': 'http://127.0.0.1:8080'}
        
        res = session.get('https://mbasic.facebook.com/me/')
        uri = res.request.url
        res = res.text
        
        headers = {
            'Origin': 'https://mbasic.facebook.com',
            'Referer': uri,
        }

        params = {
            'av' : cookies['c_user'],
            'eav' : re.findall('eav=([^;"]+)',res)[0][:-4],
            'refid' : re.findall('refid=([^;"]+)',res)[0]
        }

        data = {
            'fb_dtsg' : re.findall('name="fb_dtsg" value="([^"]+)',res)[0],
            'jazoest' : re.findall('name="jazoest" value="([^"]+)',res)[0],
            'privacyx':'291667064279714', # Friends
            'r2a' : re.findall('name="r2a" value="([^"]+)',res)[0],
            'xhpc_timeline' : re.findall('name="xhpc_timeline" value="([^"]+)',res)[0],
            'target' : cookies['c_user'],
            'c_src' : 'timeline_self',
            'cwevent' : 'composer_entry',
            'referrer' : 'timeline',
            'ctype' : 'inline',
            'cver' : 'amber',
            'rst_icv' : '' ,
            'xc_message' : status, 
            'view_post' :'Post'
        }
        
        session.post('https://mbasic.facebook.com/composer/mbasic/', params=params,data=data,headers=headers)
        return True
    except:
        return False

def mk_status():
    res = requests.get(STATUS_URL)
    if not str(res.status_code).startswith('2'):
        return False, None
    lines = [i.strip() for i in res.text.split('\n') if i.strip()]
    return True, random.choice(lines)

def main():
    success, status = mk_status()
    if not success:
        return
    cookies = get_cookies()
    if not cookies:
        return
    status = post_status(status,cookies)

main()

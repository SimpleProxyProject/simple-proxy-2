from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import requests


app = FastAPI()


@app.get('/', response_class=PlainTextResponse)
async def root(url: str, device: str = 'desktop'):
    if device == 'mobile':
        user_agent = 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
    else:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

    headers = {
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
        'user-agent': user_agent
    }

    try:
        return requests.get(url, headers=headers).text
    except:
        return 'Request failed!'

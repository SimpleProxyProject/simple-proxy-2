from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
from urllib.parse import urlencode


app = FastAPI()


@app.get('/')
def root(url: str, request: Request):
    try:
        params = dict(request.query_params)
        del params['url']
        headers = dict(request.headers)
        cookies = dict(request.cookies)
        if len(params) > 0:
            url += f'?{urlencode(params)}'
        return str(requests.get(url, headers=headers, cookies=cookies, params=params, timeout=5).text)
    except:
        return 'Request failed!'

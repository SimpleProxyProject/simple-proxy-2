from fastapi import Security, Depends, FastAPI, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_403_FORBIDDEN
import requests
from urllib.parse import urlencode
import os


app = FastAPI()
SECRET_KEY = os.environ.get('APIKEY')
apikey = APIKeyHeader(name='APIKEY', auto_error=False)


def get_api_key(apikey: str = Security(apikey)):
    if apikey == SECRET_KEY or SECRET_KEY is None:
        return apikey
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail='API key not provided or invalid.')


@app.get('/', response_class=PlainTextResponse)
def root(url: str, request: Request, api_key: APIKey = Depends(get_api_key)):
    try:
        params = dict(request.query_params)
        del params['url']
        headers = dict(request.headers)
        del headers['host']
        if params.get('host'):
            headers['host'] = params.get('host')
        del headers['accept-encoding']
        headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        cookies = dict(request.cookies)
        if len(params) > 0:
            url += f'?{urlencode(params)}'
        return str(requests.get(url, headers=headers, cookies=cookies, timeout=5).text)
    except:
        return 'Request failed!'

from fastapi import Security, Depends, FastAPI, HTTPException, Request
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_403_FORBIDDEN
import requests
from urllib.parse import urlencode
import random
import os


app = FastAPI()
SECRET_KEY = os.environ.get('SIMPLEPROXYSECRET')
apikey = APIKeyHeader(name='SIMPLEPROXYKEY', auto_error=False)


def get_api_key(apikey: str = Security(apikey)):
    if apikey == SECRET_KEY or SECRET_KEY is None:
        return apikey
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail='API key not provided or invalid.')


@app.get('/', response_class=PlainTextResponse)
def root(proxyurl: str, request: Request, api_key: APIKey = Depends(get_api_key)):
    try:
        # Get query params
        params = dict(request.query_params)

        # Get headers
        headers = dict(request.headers)

        # Remove unwanted headers
        ignore_list = ['host', 'SIMPLEPROXYKEY', 'accept-encoding']
        for header in ignore_list:
            del headers[header]

        # Set custom host header if provided
        if params.get('host'):
            headers['host'] = params.get('host')

        # Set accept header
        headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

        # Set custom user agent if requested. The list has been obtained from https://whatismybrowser.com
        user_agent = None
        desktop_useragents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
            ]
        mobile_useragents = [
            'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36']
        if params.get('simpleproxy_device') == 'desktop':
            user_agent = random.choice(desktop_useragents)
        if params.get('simpleproxy_device') == 'mobile':
            user_agent = random.choice(mobile_useragents)
        if user_agent is not None:
            headers['user-agent'] = user_agent
        
        # Delete unneeded params
        del_params = ['proxyurl', 'simpleproxy_device']
        for param in del_params:
            del params[param]

        # Get cookies from request
        cookies = dict(request.cookies)

        # Encode params & update proxy URL
        if len(params) > 0:
            proxyurl += f'?{urlencode(params)}'

        # Make external request and return response
        resp = requests.get(proxyurl, headers=headers, cookies=cookies, timeout=5)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f'Request failed: {str(e)}'

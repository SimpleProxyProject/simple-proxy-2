from selenium import webdriver
import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()

@app.get('/', response_class=PlainTextResponse)
async def root(url: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
    driver.get(url)
    return driver.page_source
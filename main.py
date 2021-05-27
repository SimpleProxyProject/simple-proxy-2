from selenium import webdriver
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
driver.get('https://webhook.site/ca79d1eb-6263-4df1-a715-86f997b5b102')
print(driver.page_source)
print('Finished!')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
#option.add_argument('--disable-dev-shm-usage')
#option.add_argument("--remote-debugging-port=9222")  # this


browser = webdriver.Chrome('./chromedriver',chrome_options=option)
print("it's OK")
from selenium import webdriver
from bs4 import BeautifulSoup
import time

start_time = time.time()
BASE_URL = 'https://kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do?dtTp=movie&dtCd='
BASE_RESULT_URL = 'https://kobis.or.kr/'

# movie_code = '20218783'
movie_code = '20001337'
url = BASE_URL+movie_code

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
img_src = soup.find("a", {'class':'fl thumb'})

target_url = img_src['href']
result_url = BASE_RESULT_URL+target_url
print(result_url)
print(f"Execution_time : {time.time()-start_time}")
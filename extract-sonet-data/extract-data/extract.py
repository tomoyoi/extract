from selenium import webdriver
import time
import chromedriver_binary
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)

driver.get("https://www.so-net.ne.jp/access/hikari/au/area/search.html?refSmRcid=lis_lis_gg_ac_all_AUHK&postcodeFirst=&postcodeLast=&phoneNumberFirst=&phoneNumberSecond=&phoneNumberThird=#/postcode")

# 郵便番号入力
search_box_first = driver.find_element_by_name("postcodeFirst")
search_box_second = driver.find_element_by_name("postcodeSecond")
search_box_first.send_keys('106')
search_box_second.send_keys('0047')

# チェックボックス入力
terms = driver.find_element_by_xpath("//input[@id='area-type-MANSION']")
terms.click()

# 入力内容送信
search_box_first.submit()
search_box_second.submit()
terms.submit()
time.sleep(10)

# HTLM取得
response = requests.get("https://www.so-net.ne.jp/access/hikari/au/area/search.html?refSmRcid=lis_lis_gg_ac_all_AUHK&postcodeFirst=&postcodeLast=&phoneNumberFirst=&phoneNumberSecond=&phoneNumberThird=#/addresses")
response.encoding = 'UTF-8'
print(response.text)


# ブラウザ閉じる
# driver.close()

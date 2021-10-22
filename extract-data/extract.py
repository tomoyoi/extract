from selenium import webdriver
import time
import csv
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--single-process')
options.add_argument('--disable-application-cache')
options.add_argument('--ignore-certificate-errors')

chrome_service = webdriver.chrome.service.Service(
    executable_path=ChromeDriverManager().install()
)
driver = webdriver.Chrome(service=chrome_service, options=options)

# 郵便番号csv読み込み
csv_file = open("37KAGAWA.CSV", "r", encoding="UTF-8", errors="ignore")
postcode_file = csv.reader(
    csv_file,
    delimiter=",",
    doublequote=True,
    lineterminator="\r\n",
    quotechar='"',
    skipinitialspace=True,
)

# csv出力
with open("./sonet_list.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["郵便番号", "住所", "建物", "種類"])

for row in list(postcode_file):
    results = []
    postcode = row[2]
    postcodeFirst = row[2][:3]
    postcodeLast = row[2][3:]

    driver.get("https://www.so-net.ne.jp/access/hikari/au/area/")
    driver.implicitly_wait(10)

    # ラジオボックス入力
    elements = driver.find_elements_by_xpath(
        "//input[@name='selectCourseKind'][@type='radio']"
    )
    for elem in elements:
        if elem.get_attribute("value") == "AUHK02":
            driver.execute_script("arguments[0].click();", elem)

    # 郵便番号入力
    search_box_first = driver.find_element_by_name("postcodeFirst")
    search_box_second = driver.find_element_by_name("postcodeLast")
    search_box_first.send_keys(postcodeFirst)
    search_box_second.send_keys(postcodeLast)

    # 入力内容送信
    search_box_first.submit()
    search_box_second.submit()

    # HTML取得
    code_url = "https://www.so-net.ne.jp/access/hikari/au/area/search.html?refSmRcid=lis_lis_gg_ac_all_AUHK&postcodeFirst=&postcodeLast=&phoneNumberFirst=&phoneNumberSecond=&phoneNumberThird=#/addresses"
    driver.get(code_url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "panel-body")))
    code = driver.find_element(by=By.CLASS_NAME, value="panel-body")
    text = code.get_attribute("innerText")
    text_list = text.split("\n")[2:-1]

    if len(text_list) == 0:
        results.append(
            [
                postcode,
                "該当なし",
            ]
        )

        with open("./sonet_list.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerows(results)

        time.sleep(1)
        continue

    for i in range(0, len(text_list), 2):
        building_name = text_list[i + 1]
        (building_name1, building_name2) = building_name.split("(")
        building_name2 = "".join(list(building_name2)[:-1])

        tmp_list = [postcode, text_list[i], building_name1, building_name2]
        results.append(tmp_list)

    with open("./sonet_list.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    time.sleep(1)

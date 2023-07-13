import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Chrome WebDriver 설정
options = Options()
# options.add_argument("--headless")  # 화면에 브라우저가 나타나지 않도록 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 페이지 접속
start_url = "https://www.gbe.kr/news/na/ntt/selectNttInfo.do?mi=17643&bbsId=4744&nttSn=1324009"
driver.get(start_url)

# 파일 다운로드
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div[2]/div[2]/ol/li[1]/ul/li[2]/span")))
    if "hwp" in element.text:
        download_button = driver.find_element(By.XPATH, '//*[@id="button_download"]')
        download_url = download_button.get_attribute("href")
        driver.execute_script("window.open('" + download_url + "');")
        time.sleep(2)  # 새 창이 로드되기까지 충분한 시간을 기다립니다.
        driver.switch_to.window(driver.window_handles[-1])  # 새 창으로 전환
except:
    print("파일 다운로드 실패")

# 다음 글로 이동
try:
    next_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subContent"]/div[2]/nav/ul/li/a/span')))
    next_link.click()
except:
    print("다음 글로 넘어가기 실패")

# 페이지 소스코드 가져오기
page_source = driver.page_source

# 필요한 작업 수행
text = driver.find_element(By.XPATH, '//*[@id="subContent"]/div[2]/nav/ul/li/a/span').text.strip()
print("다음 글로 넘어갈 텍스트:", text)

# WebDriver 종료
driver.quit()

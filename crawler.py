import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request


# Chrome WebDriver 설정
options = Options()
options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

codes=[]
counter = 1
times=3
nttsn=1324009
url = f"https://www.gbe.kr/news/na/ntt/selectNttInfo.do?mi=17643&bbsId=4744&nttSn={nttsn}"

#폴더 생성
# 새로운 폴더명
new_folder_name = "보도자료"

# 새로운 폴더 경로 생성
new_folder_path = os.path.join(os.getcwd(), new_folder_name)

# 폴더 생성
os.makedirs(new_folder_path, exist_ok=True)

#코드와 타이틀 받아오기
def get_code(url):
    # 페이지에 접속하여 HTML 가져오기
    driver.get(url)
    time.sleep(2)

    html = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    # 요소를 찾아서 텍스트 가져오기
    #//*[@id="nttViewForm"]/div[1]/table/tbody/tr[7]/td/ul/li[1]/a
    element = soup.find("ul", {"class":"file"}).find("a",attrs={"class":"btn_view"})
    title_li = soup.find("ul", {"class":"file"}).find("li")
    title = title_li.get_text(strip=True).split(".")[0]
    click_value = element['onclick'].split("'")[1]

    return click_value, title

def download_File(code,title,counter):
    # 파일 URL
    file_url = "https://www.gbe.kr/common/nttFileDownload.do?fileKey="+code
    file_name = title + ".hwp"
    # 파일 다운로드 경로 지정
    file_path = os.path.join(new_folder_path, os.path.basename(file_name))

    # 파일 다운로드
    urllib.request.urlretrieve(file_url, file_path)

    print(f"{title} 다운로드가 완료되었습니다. 다운로드: {counter}개")

while counter < 5001:
    try:
        click_value, title = get_code(url)
        download_File(click_value, title, counter)
    # 다음 페이지로 이동하기
    except:
        print(f"{nttsn}번 게시물이 없습니다.")
        counter -= 1
    nttsn -= 1
    counter += 1
    url = url = f"https://www.gbe.kr/news/na/ntt/selectNttInfo.do?mi=17643&bbsId=4744&nttSn={nttsn}"
# # 페이지 로딩을 위해 충분한 대기 시간 설정
# time.sleep(5)

# # 드라이버 종료
# driver.quit()

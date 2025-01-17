## pip install webdriver-manager 필요

## 모든 경로는 상대 경로로 설정해 두었으므로 수정 필요
# 해당 py 파일이 실행되는 경로에서 결과 파일 생성

from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 필요한 함수 생성

def html_par(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
        
    cols = soup.select('dl dt')
    els = soup.select('dl dd')
    
    return cols, els

def list_text(cols, els):
    cols_list = list()
    els_list = list()
        
    for t in cols:
        cols_list.append(t.text)
            
    for t in els:
        els_list.append(t.text)
        
    return cols_list, els_list

# file name 추출 
def name_sq(f):
    name = os.path.basename(f)
    name = os.path.splitext(name)[0]
    return name

# 기본 webdriver
driver = webdriver.Chrome()

# 기본 URL
url = "https://www.ncbi.nlm.nih.gov/datasets/genome/"

# excel 제작
def make_excel(file_s):
    file = file_s  # 읽을 파일
    with open(file, 'r') as file:
        GCA_acc = [line.strip() for line in file.readlines()]

    GCA_acc = [e for e in GCA_acc if e]  # 공백 제거 

    no_url = []  # URL 생성이 안 될 경우 쓸 list
    no_type = []  # type이 아닐 시 쓸 list

    # df 생성
    result = pd.DataFrame(columns=['Give number', 'Type', 'Submitted GenBank assembly', 'Taxon', 'Strain', 'Url'])

    for GCA in GCA_acc:
        driver.get(url + GCA)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//dt[contains(text(), 'Relation to type material')]")))

            cols, els = html_par(driver)
            cols_list, els_list = list_text(cols, els)

            # Relation to type material 여부 2차 검색
            if 'Relation to type material' in cols_list:
                d = dict(zip(cols_list, els_list))
                data = [GCA, 'yes', d.get('Submitted GenBank assembly'), ' '.join(d.get('Taxon').split()[:2]), d.get('Strain'), url + GCA]
                result.loc[len(result)] = data
        except:
            cols, els = html_par(driver)

            # 존재하지 않는 url
            if len(cols) == 0 or len(els) == 0:
                no_url.append([GCA, url + GCA])
            else:
                # url은 있으나 type이 NO
                cols_list, els_list = list_text(cols, els)

                if 'Relation to type material' not in cols_list:
                    no_type.append(dict(url=url + GCA, give_number=GCA))

    for dic in no_type:
        data = [dic.get('give_number'), 'No', None, None, None, dic.get('url')]
        result.loc[len(result)] = data
    
    for e in no_url:
        data = [e[0], None, None, None, None, 'bad_url : ' + e[1]]
        result.loc[len(result)] = data

    # 결과 파일 저장할 폴더 생성
    os.makedirs('output_02_Filtering_Type', exist_ok=True)
    # save 경로
    save_p = './output_02_Filtering_Type/'
    name = name_sq(file_s)
        
    # file name 지정
    file_name = os.path.join(save_p, name + '.xlsx')
    print(file_name)

    result.to_excel(file_name, index=False)

# 직접 지정된 파일 경로
input_path = './output_01_WGS_acc/test_WGS_acc.txt'
make_excel(input_path)

driver.close()  # 닫음

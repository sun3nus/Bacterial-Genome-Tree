from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 기본 webdriver 설정
driver = webdriver.Chrome()

# 기본 URL 설정
search_url = "https://www.ncbi.nlm.nih.gov/search/all/?term="
genome_url_prefix = "https://www.ncbi.nlm.nih.gov"

# 함수 정의: NCBI 검색 결과에서 데이터셋 링크 및 상태 확인
def fetch_dataset_link(driver, species):
    query = '+'.join(species)  # 두 단어로 구성된 species를 +로 결합
    full_url = f"{search_url}{query}"
    driver.get(full_url)
    
    try:
        # 페이지가 로드될 때까지 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.nwds-list"))
        )
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 데이터셋 링크 확인
        dataset_link_tag = soup.select_one("a#search_db_datasets")
        status_tag = soup.select_one("a#search_db_datasets > span.mdc-chip.nwds-chip.nwds-chip--label.result-count.status-200")
        
        if dataset_link_tag and status_tag:
            dataset_link = dataset_link_tag['href']
            return dataset_link, "Existence"
        else:
            return None, "Nonexistent"
    except Exception as e:
        print(f"Error processing '{species}' at {full_url}: {e}")
        return None, "Nonexistent"

# 함수 정의: 데이터셋 페이지에서 GCF 링크 및 type material 확인
def fetch_gcf_and_type(driver, dataset_link):
    if not dataset_link.startswith("http"):
        full_url = f"{genome_url_prefix}{dataset_link}"
    else:
        full_url = dataset_link

    driver.get(full_url)
    
    try:
        # GCF 링크 확인
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.MuiLink-root[href*='/datasets/genome/GCF_']"))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        gcf_link_tag = soup.select_one("a.MuiLink-root[href*='/datasets/genome/GCF_']")
        if gcf_link_tag:
            gcf_link = f"{genome_url_prefix}{gcf_link_tag['href']}"

            # GCF 링크 페이지에서 type material 확인
            driver.get(gcf_link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//dt[contains(text(), 'Relation to type material')]"))
            )

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # HTML 데이터 파싱
            cols = soup.select('dl dt')
            els = soup.select('dl dd')
            cols_list = [t.text for t in cols]
            els_list = [t.text for t in els]

            if 'Relation to type material' in cols_list:
                type_material = "yes"
            else:
                type_material = "no"

            return gcf_link, type_material
        else:
            return None, "No GCF link found"
    except Exception as e:
        print(f"Error fetching GCF link from {full_url}: {e}")
        return None, "Error"

# 입력 엑셀 파일 처리 함수
def process_excel(input_file, output_file_name):
    df = pd.read_excel(input_file)

    # 크롤링 결과를 저장할 리스트
    whole_genome_status_list = []
    type_material_list = []
    gcf_link_list = []
    accession_number_list = []

    for species in df['Missing Species']:
        species_terms = species.split()
        if len(species_terms) >= 2:
            dataset_link, status = fetch_dataset_link(driver, species_terms[:2])
            whole_genome_status_list.append(status)
            
            if dataset_link and status == "Existence":
                gcf_link, type_material = fetch_gcf_and_type(driver, dataset_link)
                gcf_link_list.append(gcf_link)
                type_material_list.append(type_material)

                # Accession number 추출
                if gcf_link:
                    accession_number = gcf_link.rstrip('/').split('/')[-1]
                    accession_number_list.append(accession_number)
                else:
                    accession_number_list.append(None)
            else:
                gcf_link_list.append(None)
                type_material_list.append(None)
                accession_number_list.append(None)
        else:
            whole_genome_status_list.append("Invalid Name")
            gcf_link_list.append(None)
            type_material_list.append(None)
            accession_number_list.append(None)

    # 데이터프레임 업데이트
    df['Whole genome'] = whole_genome_status_list
    df['Type'] = type_material_list
    df['Accession number'] = accession_number_list
    df['GCF Link'] = gcf_link_list

    # 결과 저장
    output_dir = os.path.join(os.getcwd(), "output_03_WGS")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_file_name)
    df.to_excel(output_file, index=False)
    print(f"저장된 파일: {output_file}")


# 입력 파일 경로와 출력 파일 이름 설정
input_file_path = "output_02_Comparison/test_missing_species.xlsx"
output_file_name = "test_missing_sp_Type_GCA.xlsx"  # 사용자 정의 출력 파일 이름

# 함수 실행
process_excel(input_file_path, output_file_name)

# 드라이버 닫기
driver.quit()

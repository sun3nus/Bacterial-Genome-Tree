# Bacterial-Genome-Tree

## 0. Introduction
세균 신종 논문에서 whole genome tree를 포함하는 것은 점차 필수적인 요구사항이 되고 있습니다. 신뢰할 수 있는 bacterial whole genome tree를 구축하기 위해서는 **GTDB-Tk**와 **UBCG** 도구를 사용하는 것이 권장됩니다.

### GTDB-Tk란?
**GTDB-Tk**는 Genome Taxonomy Database (GTDB)를 기반으로 유전체 데이터를 표준화된 분류 체계에 따라 분석할 수 있는 도구입니다. 이 도구는 대규모 유전체 데이터셋을 효과적으로 처리할 수 있으며, 지속적으로 업데이트되는 데이터베이스를 활용해 보다 정확하고 포괄적인 계통학적 분석을 제공합니다. 또한, NCBI에서 제공하는 whole genome 데이터를 포함하므로 신종 균주의 계통학적 위치를 정밀하게 파악하는 데 유용합니다. 그러나 GTDB-Tk는 type strain뿐만 아니라 type strain이 아닌 균주의 whole genome도 포함하고 있다는 한계가 있습니다.

### UBCG란?
**UBCG** (Up-to-date Bacterial Core Gene)는 박테리아의 계통 발생을 분석하기 위해 특정한 핵심 유전자 집합을 사용하는 계통수 구축 도구입니다. 이 도구는 박테리아 유전체에서 선택된 92개의 핵심 유전자를 사용하여 계통 분석을 수행하여 계통수를 빠르고 효율적으로 구축할 수 있습니다. UBCG를 통해 생성된 계통수는 박테리아 간의 진화적 관계를 명확히 할 수 있으며, 박테리아의 분류와 신종 인식에 중요한 정보를 제공합니다. 

### GTDB-Tk와 UBCG의 병행 사용의 필요성
세균 신종 논문에서는 type strain만을 포함하여 계통수를 구축하는 것이 원칙이므로, GTDB-Tk 결과에서 type strain만 필터링한 후 UBCG를 사용해 whole genome tree를 재구축 할 필요성이 있습니다. 결론적으로, GTDB-Tk와 UBCG는 각각의 강점을 통해 신뢰할 수 있는 bacterial whole genome tree를 구축하는 데 필수적인 도구입니다. 

## Index
```
0. Introduction
1. GTDB-Tk
    1.1 Setup GTDB-Tk
    1.2 Run GTDB-Tk
    1.3 Generate GTDB-Tk Subtree
    1.4 Filter Type Strains and Collect GCA Acc
    1.5 Compare with LPSN Validation Type Strains List
    1.6 Download Whole Genomes of Type Strains
2. UBCG
    2.1 Setup UBCG
    2.2 Prepare Whole Genome FASTA files
    2.3 Run UBCG
    2.4 Edit UBCG tree
```

<br/>

## 1. GTDB-Tk
### 1.1 Setup GTDB-tk
#### 1.1.1 Conda 환경 생성 및 활성화
```bash
conda create -n gtdbtk_env python=3.8
conda activate gtdbtk_env
```

#### 1.1.2 필요한 채널 추가 및 우선 순위 설정
```bash
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --set channel_priority strict
```

#### 1.1.3 GTDB-Tk 설치
```bash
conda instasll -c bioconda gtdbtk
```

#### 1.1.4 데이터 다운로드 및 압축해제
```bash
wget https://data.gtdb.ecogenomic.org/releases/latest/auxillary_files/gtdbtk_data.tar.gz
tar –xvzf gtdbtk_data.tar.gz
```

#### 1.1.5 Conda 환경 변수 설정
- conda env config vars set GTDBTK_DATA_PATH="your_path"
- 압축해제한 gtdbtk_data 디렉토리의 위치를 "your_path"에 입력합니다.
```bash
conda env config vars set GTDBTK_DATA_PATH="/home/biotech/BI_2024/GTDB-tk/gtdbtk_data”
source ~/.bashrc
```

#### 1.1.6 GTDB-tk 환경 활성화
```bash
conda activate gtdbtk_env
```

<br/>

### 1.2 Run GTDB-tk
#### 1.2.1 raw data 준비
- 생성된 fasta 디렉토리에 GTDB-Tk tree를 그릴 신종 균주의 whole genome fasta 파일을 넣습니다.
- 이 fasta 파일이 GTDB-Tk의 input 파일입니다.
```bash
mkdir fasta
```
```bash
ls fasta
$ test.fasta
```

#### 1.2.2 output 디렉토리 생성
```bash
mkdir classify_result
```

#### 1.2.3 Classify Workflow
```bash
gtdbtk classify_wf -x fasta --genome_dir fasta/ --out_dir classify_result/ --cpus 3 --skip_ani_screen
```
- cf. 옵션 “-x”는 input 파일의 확장자로, 만약 확장자가 fna일 경우, “-x fna”로 지정

#### 1.2.4 Convert to ITOL
- convert_to_itol 명령은 Newick 계통수를 [iTOL](https://itol.embl.de/)에서 시각화할 수 있도록 적합하게 만듭니다.
```bash
mkdir itol
```
```bash
gtdbtk convert_to_itol --input ./classify_result/classify/gtdbtk.bac120.classify.tree.3.tree --output ./itol/test_itol.tree
```

#### GTDB-Tk 실행 단계에서 Error 발생 시 해결 방법
1. 에러 메세지: pplacer is not on the system path
```bash
conda install -c bioconda pplacer
export PATH=$PATH:/path/to/pplacer
source ~/.bashrc
```

2. 에러 메세지: fastANI is not on the system path
```bash
conda install -c bioconda fastani
export PATH=$PATH:/path/to/fastani
source ~/.bashrc
```

3. conda가 없다면
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh → enter → yes → re-start
conda update conda
```
<br/>

### 1.3 Generate GTDB-tk sub-tree
#### 1.3.1 Visulation GTDB-Tk tree in iTOL
1. [iTOL](https://itol.embl.de/)에서 **Uploade** 로 들어가 GTDB-Tk 실행 최종 결과 tree 파일을 업로드합니다.

2. 계통수와 함께 나타나는 우측의 **controal Panel**에서 **Advanced** 클릭 후, "Other functions"에서 "GTDB"를 클릭합니다.
<br/> → 기존에 GCA/GCF accesion number 였던 ID가 species 이름으로 변경됩니다.

3. 로딩 후 나오는 메세지에 **Reload page** 클릭 후, **Control panel**의 **Basic** 클릭, **Mode**에서 **Rectangular**을 클릭합니다.
4. 좌측 돋보기 모양 중 **Search tree nodes**를 클릭하여 GTDB-Tk의 input fasta 파일의 이름을 검색합니다.
5. 검색 결과 Node ID를 클릭하면, 게통수를 작성하고자 input으로 넣어준 신종균주의 위치로 이동하게 됩니다.
6. 삼각형으로 축소되어 있는 경우, 좌클릭하여 **Expand clade**를 클릭합니다.
7. 계통수를 그리고자 하는 신종 균주가 속한 genus의 시작과 끝 species의 Node ID를 복사합니다.

#### 1.3.2 Generate GTDB-Tk sub-tree
1. <span style="background-color:#fff5b1"> *01_GTDB-Tk_subtree.py* </span> 에서 **tree_file**와 **output_file** 변수에 각각 GTDB-Tk 실행 최종 결과 tree 파일의 위치와, 생성된 sub-tree 파일을 저장할 위치를 입력합니다.
    * :bulb: GTDB-Tk/S1.SubTree/input 디렉토리에 GTDB-Tk 실행 최종 결과 tree 파일을 넣기
    * :bulb: 아래 스크립트의 **3. 파일 위치 설정**에서 test_itol.tree, test_subtree.nwk 이름을 수정
2. **target_taxa** 리스트 변수에 iTOL에서 복사한 genus의 시작과 끝 species의 Node ID를 입력합니다.
3. <span style="background-color:#fff5b1"> *01_GTDB-Tk.subtree.py* </span> 실행합니다.
```python
## 1. Biopython 환경설정 ##
#pip install biopython
import Bio
from Bio import Phylo

## 2. 서브트리 생성 함수 ##
def extract_subtree(tree_file, output_file, target_taxa):
    # 트리 파일을 로드
    tree = Phylo.read(tree_file, "newick")

    # 공통 조상 찾기
    common_ancestor = tree.common_ancestor(target_taxa)

    # 서브트리 추출
    subtree = Phylo.BaseTree.Tree(root=common_ancestor)

    # 서브트리 저장
    Phylo.write(subtree, output_file, "newick")

## 3. 파일 위치 설정 ##
tree_file = 'input/test_itol.tree'
output_file = 'output/test_subtree.nwk'

## 4. 서브트리 시작, 위치 설정 ##
# target_taxa = ['시작 어세션 넘버', '끝 어세션 넘버']
target_taxa = ['GB_GCA_002482885.1', 'RS_GCF_900101855.1'] 

## 5. 서브트리 생성 ##
extract_subtree(tree_file, output_file, target_taxa)
```

<br/>

### 1.4 Filter Type Strains and Collect GCA Acc
#### 1.4.1 Extract Genome Accesion Number in Sub-tree
1. <span style="background-color:#fff5b1"> *02_extract_WGS_acc.py* </span> 에서 **nwk_file_path** 변수에 앞서 생성한 sub-tree 파일의 위치를 입력합니다.
2. **output_file_path** 변수에 결과 파일의 위치와 이름을 입력합니다.
3. <span style="background-color:#fff5b1"> *02_extract_WGS_acc.py* </span> 를 실행합니다.
4. 실행 결과, sub-tree 안의 모든 species의 genome accession number가 txt 파일 형식으로 추출됩니다.
```python
# nwk 파일에서 'RS' 또는 'GB'로 시작하는 문자열을 ':' 문자 이전까지 추출하고, 
# 'RS_' 또는 'GB_'를 제거하여 저장

# 파일 위치 설정
nwk_file_path = '../S1. SubTree/output/test_subtree.nwk'

prefix_strings_revised = []
with open(nwk_file_path, 'r') as file:
    for line in file:
        # 괄호와 쉼표를 포함하여 문자열을 분리
        items = line.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
        for item in items:
            # 'RS' 또는 'GB'로 시작하는 문자열 추출
            if item.startswith(('RS', 'GB')):
                # ':' 문자 이전까지의 문자열 추출
                prefix = item.split(':')[0]
                # 'RS_' 또는 'GB_' 제거
                cleaned_prefix = prefix[3:]
                prefix_strings_revised.append(cleaned_prefix)

# 결과 확인
prefix_strings_revised[:10], len(prefix_strings_revised)  # 처음 10개 항목과 총 개수 출력

# 결과 리스트를 텍스트 파일로 저장
output_file_path = './output_01_WGS_acc/test_WGS_acc.txt'
with open(output_file_path, 'w') as file:
    for prefix in prefix_strings_revised:
        file.write(prefix + '\n')
```

#### 1.4.2 Filter Type Strains
1. *03_extract_Type_strains.py* 에서 **input_path** 변수에 앞서 생성한 genome accession number txt 파일의 위치를 입력합니다.
2. *03_extract_Type_strains.py*를 실행합니다.
3. 실행 결과, input txt 파일 이름과 동일한 엑셀 파일이 형성되며, 이 엑셀 파일은 "Give number", "Type", "Submitted GenBank assembly", "Taxon", "Strain", "Url" 열로 구성되어 있습니다.
4. "Type" 열이 **yes**인 균주들의 whole genome fasta 파일로 추후 UBCG tree 를 구축할 예정입니다.
```python
# 파일 위치 설정
nwk_file_path = '../S1. SubTree/output/test_subtree.nwk'

prefix_strings_revised = []
with open(nwk_file_path, 'r') as file:
    for line in file:
        # 괄호와 쉼표를 포함하여 문자열을 분리
        items = line.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
        for item in items:
            # 'RS' 또는 'GB'로 시작하는 문자열 추출
            if item.startswith(('RS', 'GB')):
                # ':' 문자 이전까지의 문자열 추출
                prefix = item.split(':')[0]
                # 'RS_' 또는 'GB_' 제거
                cleaned_prefix = prefix[3:]
                prefix_strings_revised.append(cleaned_prefix)

# 결과 확인
prefix_strings_revised[:10], len(prefix_strings_revised)  # 처음 10개 항목과 총 개수 출력

# 결과 리스트를 텍스트 파일로 저장
output_file_path = './output_WGS_acc/test_WGS_acc.txt'
with open(output_file_path, 'w') as file:
    for prefix in prefix_strings_revised:
        file.write(prefix + '\n')
```
<br/>

### 1.5 Compare with LPSN Validation Type Strains List
GTDB-Tk 데이터베이스는 지속적으로 업데이트되지만 많은 양의 신종 세균이 빠르게 업데이트 되기 때문에 모든 균주의 데이터를 포함하고 있지는 못합니다. <br/>

따라서 LPSN과 같은 validly published된 원핵생물(세균 및 고세균)의 공식적인 정보를 제공하는 온라인 데이터베이스와 GTDB-Tk 데이터베이스에서 필터링된 데이터를 비교할 필요가 있습니다.

1. [LSPN](https://www.bacterio.net/)에 계통수를 구축하고자 하는 신종 균주의 genus를 입력합니다.
2. Child taxa 표를 복사하여 새로운 엑셀 파일을 만듭니다. 파일 이름은 “속이름_LPSN_list.xlsx”로 하고, S3.CompareToLPSN 디렉토리의 input 폴더에 저장합니다.
3. *04_LPSN_GTDB_Species_Comparison.py*에서 **file_path_LPSN**에 방금 생성한 엑셀 파일의 위치를 지정합니다.
3. *04_LPSN_GTDB_Species_Comparison.py*를 실행합니다.

<br/>

#### 1.5.1 LPSN species list에서 validly published된 species만 필터링합니다.

* "Nomenclatural status" 열이 "validly published under the ICNP"인 데이터 중에는 "Taxonomic status"가 "correct name"과 "Synonym"인 것이 있는데, Synonym은 이전 명칭이므로 correct name인것만 필터링해야 합니다. <br/>
```python
import pandas as pd
import os

# input file 경로 설정 (사용자가 지정)
file_path_LPSN = 'input/Genus_LPSN_list.xlsx'
file_path_GTDB = '../S2. ExtractType/ouptut_02_Filtering_Type/test_WGS_acc.xlsx'

# 결과를 저장할 디렉터리 생성 (없으면 생성)
os.makedirs("output_01_LPSN", exist_ok=True)
os.makedirs("output_02_Comparison", exist_ok=True)
os.makedirs("output_03_WGS", exist_ok=True)

# input file 읽기
LPSN_df = pd.read_excel(file_path_LPSN)
GTDB_df = pd.read_excel(file_path_GTDB)

### 1. LPSN 데이터에서 validly published된 correct name 필터링

# "Taxonomic status" 값이 "correct name"인 행만 필터링
LPSN_df_filtered = LPSN_df[LPSN_df['Taxonomic status'] == 'correct name']

# "Name" 열의 앞 두 단어만 추출 -> 종 속 명만 추출
LPSN_df_filtered['Name'] = LPSN_df_filtered['Name'].apply(lambda x: ' '.join(x.split()[:2]))

# 총 데이터 개수 확인
total_count = len(LPSN_df_filtered)
print("LPSN validly published species 개수: ", total_count)

# 수정된 데이터프레임을 새로운 엑셀 파일로 저장
output_file_path_01 = 'output_01_LPSN/Genus_LPSN_validation_list.xlsx'
LPSN_df_filtered.to_excel(output_file_path_01, index=False)
```
#### 1.5.2 LPSN과 GTDB-Tk 데이터의 validly published species 리스트를 비교하여 GTDB-Tk에서 누락된 species를 추출합니다.
```python
### 2. LPSN validly published species 리스트와 GTDB-Tk 데이터 비교

# "Name" 열과 "Taxon" 열 추출
LPSN_names = LPSN_df['Name'].dropna().unique()
GTDB_names = GTDB_df['Taxon'].dropna().unique()

# LPSN 데이터에는 있지만 GTDB 데이터에는 없는 species 추출
missing_species = [name for name in LPSN_names if name not in GTDB_names]

# 결과를 DataFrame으로 저장
missing_species_df = pd.DataFrame(missing_species, columns=['Missing Species'])

# 결과를 엑셀 파일로 저장
output_file_path_02 = "output_02_Comparison/Genus_missing_species.xlsx"
missing_species_df.to_excel(output_file_path_02, index=False)
```

#### 1.5.3 NCBI 웹 크롤링을 통해 GTDB-Tk에서 누락된 validly published species의 whole genome 데이터 유무를 확인하고, 데이터가 존재할 경우 Type 확인 및 accession number를 추출합니다.
1. *05_extract_Type_in_missing_sp.py*에서 **input_file_path**와 **output_file_path** 변수에 각각 *04_LPSN_GTDB_Species_Comparison.py* 최종 실행 결과 파일의 위치와 *05_extract_Type_in_missing_sp.py* 실행 결과 파일이 저장될 위치를 입력합니다.
2. *05_extract_Type_in_missing_sp.py*를 실행합니다.
    - *05_extract_Type_in_missing_sp.py* 실행 결과 파일은 "Missing Species", "Whole genome", "Type", "Accession number", "GCF Link" 열로 구성됩니다.
    - NCBI에서 TDB-Tk 에서 누락된 종의 whole genome 데이터를 찾고, whole genome 데이터가 있을 경우, 해당 데이터가 type 인지의 유무와 accession number를 제공합니다.
```python
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
```

<br/>

### 1.6 Download Whole Genomes of Type Strains
이제 마지막으로 지금까지 필터링하고 추출한 type strains의 whole genome 데이터를 다운로드 받아 UBCG tree를 그릴 준비를 마무리합니다.

아래 두 파일이 이 과정을 위해 필요한 최종 파일입니다.
- S2. ExtractType\output_02_Filtering_Type\test_WGS_acc.xlsx
- S3. CompareToLPSN\output_03_WGS\test_missing_sp_Type_GCA.xlsx

#### 1.6.1 전처리 
1. 두 엑셀 파일에서 에러 메세지가 표시되어 있거나 NA 값이 있는 경우 NCBI에 재검색하여 데이터를 처리합니다.
2. 두 엑셀 파일에서 Type인 strains의 GCA 또는 GCF accession number만 모아 중복 검사를 시행합니다.
3. 전처리된 accession number를 모아 텍스트 파일에 붙여넣습니다.

#### 1.6.2 Whole genome 계통수를 그릴 신종 균주의 genus의 모든 type strains의 whole genome 얻기
1. [Batch Entrez](https://www.ncbi.nlm.nih.gov/sites/batchentrez)에서 Database를 “Assembly”로 선택한 후, File에 생성한 텍스트 파일 업로드 후, “Retreive”하여 whole genome 시퀀스 파일을 다운로드합니다.




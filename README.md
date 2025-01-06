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
    1.4 Filter Type Species and Collect GCA Acc
    1.5 Compare with LPSN Validation Type Species List
    1.6 Download Whole Genomes of Type Species
2. UBCG
    2.1 Setup UBCG
    2.2 Prepare Whole Genome FASTA files
    2.3 Run UBCG
    2.4 Edit UBCG tree
```


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
5. 검색 결과 Node ID를 클릭하면, 게통수를 작성하고자 input으로 넣어준 신종주의 위치로 이동하게 됩니다.
6. 삼각형으로 축소되어 있는 경우, 좌클릭하여 **Expand clade**를 클릭합니다.
7. 계통수를 그리고자 하는 신종 균주가 속한 genus의 시작과 끝 species의 Node ID를 복사합니다.

#### 1.3.2 Generate GTDB-Tk sub-tree
1. *01_GTDB-Tk_subtree.py* 에서 **tree_file** 변수에 GTDB-Tk 실행 최종 결과 tree 파일의 위치와 **output_file** 변수에 저장될 output 파일의 위치와 이름을 입력합니다.
2. **target_taxa** 리스트 변수에 iTOL에서 복사한 genus의 시작과 끝 species의 Node ID를 입력합니다.
3. *01_GTDB-Tk.subtree.py* 실행합니다.

<br/>

### 1.4 Filter Type Species and Collect GCA Acc
#### 1.4.1 Extract Genome Accesion Number in Sub-tree
1. *02_extract_WGS_acc.py* 에서 **nwk_file_path** 변수에 앞서 생성한 sub-tree 파일의 위치를 입력합니다.
2. **output_file_path** 변수에 결과 파일의 위치와 이름을 입력합니다.
3. *02_extract_WGS_acc.py* 를 실행합니다.
4. 실행 결과, sub-tree 안의 모든 species의 genome accession number가 txt 파일 형식으로 추출됩니다.

#### 1.4.2 Filter Type species
1. *03_extract_Type_species.py* 에서 **input_path** 변수에 앞서 생성한 genome accession number txt 파일의 위치를 입력합니다.
2. *03_extract_Type_species.py*를 실행합니다.
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

### 1.5 Compare with LPSN Validation Type Species List
GTDB-Tk 데이터베이스는 지속적으로 업데이트되는 되지만 많은 양의 신종 세균이 빠르게 업데이트 되기 때문에 모든 균주의 데이터를 포함하고 있지는 못합니다. <br/>

따라서 LPSN과 같은 validly published된 원핵생물(세균 및 고세균)의 공식적인 정보를 제공하는 온라인 데이터베이스에서 genus에 속한 species list와 비교할 필요가 있습니다.
 


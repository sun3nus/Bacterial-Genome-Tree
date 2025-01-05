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
1. Conda 환경 생성 및 활성화
```bash
conda create -n gtdbtk_env python=3.8
conda activate gtdbtk_env
```

2. 필요한 채널 추가 및 우선 순위 설정
```bash
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --set channel_priority strict
```

3. GTDB-Tk 설치
```bash
conda instasll -c bioconda gtdbtk
```

4. 데이터 다운로드 및 압축해제
```bash
wget https://data.gtdb.ecogenomic.org/releases/latest/auxillary_files/gtdbtk_data.tar.gz
tar –xvzf gtdbtk_data.tar.gz
```

5. Conda 환경 변수 설정
- conda env config vars set GTDBTK_DATA_PATH="your_path"
- 압축해제한 gtdbtk_data 디렉토리의 위치를 "your_path"에 입력합니다.
```bash
conda env config vars set GTDBTK_DATA_PATH="/home/biotech/BI_2024/GTDB-tk/gtdbtk_data”
source ~/.bashrc
```

6. GTDB-tk 환경 활성화
```bash
conda activate gtdbtk_env
```


## 1.2 Run GTDB-tk
1. raw data 준비
- 생성된 fasta 디렉토리에 GTDB-Tk tree를 그릴 신종 균주의 whole genome fasta 파일을 넣습니다.
- 이 fasta 파일이 GTDB-Tk의 input 파일입니다.
```bash
mkdir fasta
```

2. output 디렉토리 생성
```bash
mkdir classify_result
```

3. Classify Workflow
```bash
gtdbtk classify_wf -x fasta --genome_dir fasta/ --out_dir classify_result/all --cpus 3 --skip_ani_screen
```
- cf. 옵션 “-x”는 input 파일의 확장자로, 만약 확장자가 fna일 경우, “-x fna”로 지정

4. Convert to ITOL
- convert_to_itol 명령은 Newick 계통수를 [iTOL](https://itol.embl.de/)에서 시각화할 수 있도록 적합하게 만듭니다.
```bash
mkdir itol
```
```bash
gtdbtk convert_to_itol --input ./classify_result/classify/gtdbtk.bac120.classify.tree.3.tree --output ./itol/itol.tree
```


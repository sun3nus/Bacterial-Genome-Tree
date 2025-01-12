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

### 2. LPSN validly published species 리스트와 GTDB-Tk 데이터 비교

# "Name" 열과 "Taxon" 열 추출
LPSN_names = LPSN_df['Name'].dropna().unique()
GTDB_names = GTDB_df['Taxon'].dropna().unique()

# LPSN 데이터에는 있지만 GTDB 데이터에는 없는 species 추출
missing_species = [name for name in LPSN_names if name not in GTDB_names]

# 결과를 DataFrame으로 저장
missing_species_df = pd.DataFrame(missing_species, columns=['Missing Species'])

# 결과를 엑셀 파일로 저장
output_file_path_02 = "output_02_Comparison/test_missing_species.xlsx"
missing_species_df.to_excel(output_file_path_02, index=False)

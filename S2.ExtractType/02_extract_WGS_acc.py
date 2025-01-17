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